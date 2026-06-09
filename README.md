# Habit Tracker

A full-stack habit tracking app built with Flask, SQLite, and vanilla JS.

## Features
- Add and delete habits
- Mark habits as done each day
- Streak counter — tracks consecutive days completed
- 7-day bar chart per habit (Chart.js)
- Fully responsive

## Tech stack
- **Backend**: Python + Flask + SQLAlchemy
- **Database**: SQLite (local) 
- **Frontend**: HTML + CSS + vanilla JavaScript + Chart.js
- **Deploy**: Render

## Run locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/habit-tracker
cd habit-tracker

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Visit `http://localhost:5000` in your browser.

## API endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/habits` | List all habits with streak + done_today |
| POST | `/habits` | Create a habit `{"name": "..."}` |
| DELETE | `/habits/<id>` | Delete a habit and all its logs |
| POST | `/habits/<id>/log` | Mark habit as done today |
| GET | `/habits/<id>/stats` | Last 7 days completion data |

## Deploy to Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`
6. Deploy

> **Note**: Render's free tier uses an ephemeral filesystem — SQLite data resets on redeploy. For persistent data, swap SQLite for Render's free PostgreSQL add-on.

## Screenshots

_Add a screenshot here after your first deploy_
