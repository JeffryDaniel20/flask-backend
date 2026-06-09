from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///habits.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class HabitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    habit_id = db.Column(
        db.Integer,
        db.ForeignKey("habit.id"),
        nullable=False
    )

    date = db.Column(
        db.Date,
        nullable=False
    )


def calculate_streak(habit_id):
    logs = HabitLog.query.filter_by(
        habit_id=habit_id
    ).all()

    logged_dates = {
        log.date for log in logs
    }

    streak = 0
    current_day = date.today()

    while current_day in logged_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak


@app.route("/")
def home():
    return "Hello"


@app.route("/habits", methods=["POST"])
def create_habit():
    data = request.get_json()

    habit = Habit(name=data["name"])

    db.session.add(habit)
    db.session.commit()

    return {"message": "Habit created"}, 201


@app.route("/habits", methods=["GET"])
def get_habits():
    habits = Habit.query.all()

    result = []

    for habit in habits:
        result.append({
            "id": habit.id,
            "name": habit.name,
            "created_at": habit.created_at.isoformat(),
            "streak": calculate_streak(habit.id)
        })

    return result, 200


@app.route("/habits/<int:id>", methods=["DELETE"])
def delete_habit(id):
    habit = Habit.query.get(id)

    if habit is None:
        return {"error": "Habit not found"}, 404

    db.session.delete(habit)
    db.session.commit()

    return {"message": "Habit deleted"}, 200


@app.route("/habits/<int:id>/log", methods=["POST"])
def log_habit(id):

    habit = Habit.query.get(id)

    if habit is None:
        return {"error": "Habit not found"}, 404

    today = date.today()

    existing_log = HabitLog.query.filter_by(
        habit_id=id,
        date=today
    ).first()

    if existing_log:
        return {
            "error": "Habit already logged today"
        }, 400

    log = HabitLog(
        habit_id=id,
        date=today
    )

    db.session.add(log)
    db.session.commit()

    return {
        "message": "Habit marked as done"
    }, 201

@app.route("/habits/<int:id>/stats", methods=["GET"])
def habit_stats(id):

    habit = Habit.query.get(id)

    if habit is None:
        return {"error": "Habit not found"}, 404

    logs = HabitLog.query.filter_by(
        habit_id=id
    ).all()

    logged_dates = {
        log.date for log in logs
    }

    stats = []

    for i in range(6, -1, -1):
        day = date.today() - timedelta(days=i)

        stats.append({
            "date": day.isoformat(),
            "completed": day in logged_dates
        })

    return stats, 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)