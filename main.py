from fastapi import FastAPI
from database import engine, SessionLocal
from models import Base, Reminder, DoseLog

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/home/upcoming")
def get_upcoming_reminder():
    db = SessionLocal()
    reminder = db.query(Reminder).first()

    if not reminder:
        return {"medication": None, "time": None}

    return {
        "medication": reminder.medication_name,
        "time": reminder.time
    }

@app.post("/log-dose")
def log_dose(data: dict):
    db = SessionLocal()
    dose = DoseLog(medication_name=data["medication"])
    db.add(dose)
    db.commit()
    return {"status": "logged"}

@app.post("/check-interaction")
def check_interaction(data: dict):
    if data["alcohol"] and data["medication"].lower() == "atorvastatin":
        return {
            "severity": "Caution",
            "message": "Atorvastatin with alcohol may increase liver strain. Continue as usual."
        }

    return {
        "severity": "Safe",
        "message": "No significant interactions detected."
    }
@app.post("/home/reminder")
def create_reminder(data: dict):
    db = SessionLocal()

    reminder = Reminder(
        medication_name=data["medication"],
        time=data["time"]
    )

    db.add(reminder)
    db.commit()

    return {"status": "reminder created"}

