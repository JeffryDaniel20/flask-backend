# Flask Habit Tracker Backend

A simple Flask REST API for tracking habits, daily completions, streaks, and weekly statistics.

## Technologies Used

* Python
* Flask
* Flask-SQLAlchemy
* SQLite

## Installation

### Clone the Repository

```bash
git clone https://github.com/JeffryDaniel20/flask-backend.git
cd flask-backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install flask flask-sqlalchemy
```

### Run the Application

```bash
python app.py
```

Server URL:

```text
http://127.0.0.1:5000
```

---

# API Endpoints

## GET /

Returns a simple message.

Response:

```text
Hello
```

---

## POST /habits

Creates a new habit.

Request:

```json
{
  "name": "Exercise"
}
```

Response:

```json
{
  "message": "Habit created"
}
```

---

## GET /habits

Returns all habits.

Response:

```json
[
  {
    "id": 1,
    "name": "Exercise",
    "created_at": "2026-06-08T10:00:00",
    "streak": 4
  }
]
```

---

## DELETE /habits/<id>

Deletes a habit.

Response:

```json
{
  "message": "Habit deleted"
}
```

---

## POST /habits/<id>/log

Marks a habit as completed today.

Response:

```json
{
  "message": "Habit marked as done"
}
```

---

## GET /habits/<id>/stats

Returns completion status for the last 7 days.

Response:

```json
[
  {
    "date": "2026-06-02",
    "completed": false
  },
  {
    "date": "2026-06-03",
    "completed": true
  }
]
```

---

# Features

* Create habits
* View habits
* Delete habits
* Daily habit logging
* Duplicate log prevention
* Streak calculation
* Weekly statistics
* SQLite database storage
