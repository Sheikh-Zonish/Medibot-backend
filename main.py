from fastapi import FastAPI
from database import engine, SessionLocal
from models import Base, Reminder, DoseLog, Medication, SafetyCheckLog
from datetime import datetime, timedelta

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/home/upcoming")
def get_upcoming_reminder():
    db = SessionLocal()
    try:
        reminder = db.query(Reminder).first()

        if not reminder:
            return {"medication": None, "time": None}

        return {
            "medication": reminder.medication_name,
            "time": reminder.time
        }
    finally:
        db.close()


@app.post("/home/reminder")
def create_reminder(data: dict):
    db = SessionLocal()
    try:
        reminder = Reminder(
            medication_name=data["medication"],
            time=data["time"]
        )
        db.add(reminder)
        db.commit()
        return {"status": "reminder created"}
    finally:
        db.close()


@app.post("/log-dose")
def log_dose(data: dict):
    db = SessionLocal()
    try:
        medication_name = data["medication"]
        now = datetime.utcnow()

        start_of_day = datetime(now.year, now.month, now.day)
        end_of_day = start_of_day + timedelta(days=1)

        existing = db.query(DoseLog).filter(
            DoseLog.medication_name == medication_name,
            DoseLog.taken_at >= start_of_day,
            DoseLog.taken_at < end_of_day
        ).first()

        if existing:
            return {"status": "already_logged"}

        dose = DoseLog(medication_name=medication_name)
        db.add(dose)
        db.commit()
        return {"status": "logged"}
    finally:
        db.close()


@app.delete("/log-dose/latest")
def delete_latest_dose():
    db = SessionLocal()
    try:
        last = db.query(DoseLog).order_by(DoseLog.taken_at.desc()).first()

        if not last:
            return {"status": "no logs"}

        db.delete(last)
        db.commit()
        return {"status": "deleted"}
    finally:
        db.close()


@app.post("/seed-medications")
def seed_medications():
    db = SessionLocal()
    try:
        existing = db.query(Medication).count()
        if existing > 0:
            return {"status": "already seeded"}

        meds = [
            Medication(name="Atorvastatin", generic_info="Generic (Lipitor)", condition="Cholesterol", color_hex="#F4C542", is_suggested=1),
            Medication(name="Lisinopril", generic_info="Generic (Zestril)", condition="Hypertension", color_hex="#C084FC", is_suggested=1),
            Medication(name="Levothyroxine", generic_info="Generic (Synthroid)", condition="Thyroid", color_hex="#60A5FA", is_suggested=1),
            Medication(name="Metformin", generic_info="Generic (Glucophage)", condition="Diabetes", color_hex="#34D399", is_suggested=1),
            Medication(name="Amlodipine", generic_info="Generic (Norvasc)", condition="Hypertension", color_hex="#38BDF8", is_suggested=1),
            Medication(name="Warfarin", generic_info="Generic (Coumadin)", condition="Blood Thinner", color_hex="#F87171", is_suggested=0),
            Medication(name="Acetaminophen", generic_info="Generic (Tylenol)", condition="Pain Relief", color_hex="#FDBA74", is_suggested=0),
            Medication(name="Amoxicillin", generic_info="Generic Antibiotic", condition="Infection", color_hex="#6EE7B7", is_suggested=0)
        ]

        db.add_all(meds)
        db.commit()
        return {"status": "seeded"}
    finally:
        db.close()


@app.get("/medications")
def get_medications():
    db = SessionLocal()
    try:
        meds = db.query(Medication).all()
        return [
            {
                "id": m.id,
                "name": m.name,
                "generic_info": m.generic_info,
                "condition": m.condition,
                "color_hex": m.color_hex,
                "is_suggested": bool(m.is_suggested)
            }
            for m in meds
        ]
    finally:
        db.close()


@app.post("/check-interaction")
def check_interaction(data: dict):
    db = SessionLocal()
    try:
        medication = data.get("medication", "").lower()
        alcohol = data.get("alcohol", False)
        caffeine = data.get("caffeine", False)
        supplements = data.get("supplements", False)

        if medication == "atorvastatin" and alcohol:
            severity = "Caution"
            message = "Atorvastatin with alcohol may increase liver strain. Limit alcohol intake."
        elif medication == "warfarin" and supplements:
            severity = "High"
            message = "Warfarin with some supplements may increase bleeding risk. Seek medical advice."
        elif medication == "metformin" and alcohol:
            severity = "Caution"
            message = "Alcohol with Metformin may increase the risk of side effects. Use carefully."
        elif medication == "levothyroxine" and supplements:
            severity = "Caution"
            message = "Some supplements may affect Levothyroxine absorption. Separate dosing times."
        elif medication == "lisinopril" and supplements:
            severity = "Caution"
            message = "Certain supplements may affect blood pressure control. Review before use."
        elif medication == "amlodipine" and alcohol:
            severity = "Safe"
            message = "No major interaction detected, but monitor for dizziness."
        elif medication == "atorvastatin" and caffeine:
            severity = "Safe"
            message = "No significant interaction detected with caffeine."
        else:
            severity = "Safe"
            message = "No significant interactions detected."

        log = SafetyCheckLog(
            medication_name=data.get("medication", ""),
            severity=severity,
            message=message
        )
        db.add(log)
        db.commit()

        return {
            "severity": severity,
            "message": message
        }
    finally:
        db.close()


@app.get("/insights")
def get_insights():
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)

        dose_logs = db.query(DoseLog).filter(DoseLog.taken_at >= week_ago).all()
        reminders = db.query(Reminder).all()

        total_doses = max(len(reminders) * 7, 1)

        day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        weekly_counts = {day: 0 for day in day_names}
        unique_logged_days = set()

        for log in dose_logs:
            day = log.taken_at.strftime("%a")
            date_key = log.taken_at.date()

            if day in weekly_counts and date_key not in unique_logged_days:
                weekly_counts[day] = 1
                unique_logged_days.add(date_key)

        doses_taken = len(unique_logged_days)
        adherence_percent = min(int((doses_taken / total_doses) * 100), 100)

        weekly_doses = [
            {"day": day, "value": weekly_counts[day]}
            for day in day_names
        ]

        safety_checks_this_week = db.query(SafetyCheckLog).filter(
            SafetyCheckLog.checked_at >= week_ago
        ).count()

        return {
            "adherence_percent": adherence_percent,
            "doses_taken": doses_taken,
            "total_doses": total_doses,
            "weekly_doses": weekly_doses,
            "safety_checks_this_week": safety_checks_this_week
        }
    finally:
        db.close()



@app.get("/safety-checks")
def get_safety_checks():
    db = SessionLocal()
    try:
        checks = db.query(SafetyCheckLog).order_by(SafetyCheckLog.checked_at.desc()).all()

        return [
            {
                "id": c.id,
                "medication_name": c.medication_name,
                "severity": c.severity,
                "message": c.message,
                "checked_at": c.checked_at.isoformat()
            }
            for c in checks
        ]
    finally:
        db.close()


@app.get("/safety-checks/weekly")
def get_weekly_safety_checks():
    db = SessionLocal()
    try:
        week_ago = datetime.utcnow() - timedelta(days=7)

        checks = db.query(SafetyCheckLog).filter(
            SafetyCheckLog.checked_at >= week_ago
        ).order_by(SafetyCheckLog.checked_at.desc()).all()

        return [
            {
                "id": c.id,
                "medication_name": c.medication_name,
                "severity": c.severity,
                "message": c.message,
                "checked_at": c.checked_at.isoformat()
            }
            for c in checks
        ]
    finally:
        db.close()

