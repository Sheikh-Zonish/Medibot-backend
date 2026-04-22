# Medibot-backend – FastAPI Backend for MediBot

## Overview

This repository contains the backend component of the MediBot project. It provides the API services required by the iOS frontend, including medication retrieval, interaction checking, reminder support, dose logging, and safety insights.

The backend is developed using FastAPI and is intended to run locally for demonstration and assessment purposes.

---

## How to Run the Project

### Prerequisites

To run this backend, the following are required:

* Python 3 installed
* Terminal or command line access
* Required Python packages installed

---

### Step 1: Open the Backend Folder

Navigate to the backend project directory:

```bash
cd Medibot-backend
```

---

### Step 2: Install Dependencies

Install the required packages using:

```bash
python3 -m pip install -r requirements.txt
```

If needed, install `uvicorn` separately:

```bash
python3 -m pip install uvicorn
```

---

### Step 3: Start the Server

Run the FastAPI application using:

```bash
python3 -m uvicorn main:app --reload
```

The backend will run locally at:

```text
http://127.0.0.1:8000
```

---

### Step 4: Open the API Documentation

FastAPI provides automatic API documentation at:

```text
http://127.0.0.1:8000/docs
```

This page can be used to inspect and test all available endpoints.

---

## Important Note

This backend is intended to be used together with the MediBot iOS frontend. The frontend is configured to connect to:

```text
http://127.0.0.1:8000
```

Therefore, the backend must be running before the frontend application is launched.

Frontend repository:
Sheikh-Zonish/MediBot

---

## Main Features

The backend supports the following functionality:

* Retrieval of medication data
* Interaction checking based on medication and lifestyle factors
* Reminder retrieval and creation
* Dose logging and deletion
* Safety history retrieval
* Weekly safety summary retrieval
* Insights and adherence data retrieval

---

## API Endpoints

The main API endpoints included in this backend are:

* GET `/home/upcoming`
* POST `/home/reminder`
* POST `/log-dose`
* DELETE `/log-dose/latest`
* POST `/seed-medications`
* GET `/medications`
* POST `/check-interaction`
* GET `/insights`
* GET `/safety-checks`
* GET `/safety-checks/weekly`

---

## Project Files

```text
Medibot-backend/
├── database.py
├── main.py
├── medibot.db
├── models.py
└── requirements.txt
```

### File Description

* **main.py** – defines the FastAPI application and API routes
* **models.py** – contains the data models used by the backend
* **database.py** – handles database setup and related logic
* **medibot.db** – local database file used for demonstration
* **requirements.txt** – lists required Python dependencies

---

## How the Backend Is Used

When the backend is running, the frontend can:

1. Request the medication list
2. Submit an interaction check request
3. Retrieve insights data
4. Load safety history
5. Log or remove medication doses
6. Access reminder-related functionality

---

## Technology Stack

* Python 3
* FastAPI
* Uvicorn
* SQLite

---

## Limitations

* The backend is configured for local execution only
* It uses demonstration data and a local database
* No authentication or production deployment is included

---

## Purpose of the Project

This backend was developed to support the functionality of the MediBot iOS application and to demonstrate:

* REST API development using FastAPI
* Backend support for a mobile application
* Database-driven medication and safety features
* Integration between frontend and backend components

---

## Author

Zonish Sheikh
