from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///habits.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ─── Models ───────────────────────────────────────────────────────────────────

class Habit(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    logs       = db.relationship("HabitLog", backref="habit", lazy=True, cascade="all, delete-orphan")

    def current_streak(self):
        """Count consecutive days completed up to and including today."""
        today = date.today()
        streak = 0
        check = today
        logged_dates = {log.date for log in self.logs}
        while check in logged_dates:
            streak += 1
            check -= timedelta(days=1)
        return streak

    def to_dict(self):
        today = date.today()
        today_logged = any(log.date == today for log in self.logs)
        return {
            "id":           self.id,
            "name":         self.name,
            "created_at":   self.created_at.isoformat(),
            "streak":       self.current_streak(),
            "done_today":   today_logged,
        }


class HabitLog(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)
    date     = db.Column(db.Date, nullable=False, default=date.today)

    __table_args__ = (
        db.UniqueConstraint("habit_id", "date", name="unique_habit_date"),
    )


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/habits", methods=["GET"])
def get_habits():
    habits = Habit.query.order_by(Habit.created_at).all()
    return jsonify([h.to_dict() for h in habits]), 200


@app.route("/habits", methods=["POST"])
def create_habit():
    data = request.get_json()
    name = (data or {}).get("name", "").strip()
    if not name:
        return jsonify({"error": "Name is required"}), 400
    habit = Habit(name=name)
    db.session.add(habit)
    db.session.commit()
    return jsonify(habit.to_dict()), 201


@app.route("/habits/<int:habit_id>", methods=["DELETE"])
def delete_habit(habit_id):
    habit = db.session.get(Habit, habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404
    db.session.delete(habit)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200


@app.route("/habits/<int:habit_id>/log", methods=["POST"])
def log_habit(habit_id):
    habit = db.session.get(Habit, habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404
    today = date.today()
    already_logged = HabitLog.query.filter_by(habit_id=habit_id, date=today).first()
    if already_logged:
        return jsonify({"error": "Already logged today"}), 409
    log = HabitLog(habit_id=habit_id, date=today)
    db.session.add(log)
    db.session.commit()
    return jsonify(habit.to_dict()), 201


@app.route("/habits/<int:habit_id>/stats", methods=["GET"])
def habit_stats(habit_id):
    habit = db.session.get(Habit, habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404
    logged_dates = {log.date for log in habit.logs}
    today = date.today()
    stats = []
    for i in range(6, -1, -1):          # oldest → newest
        day = today - timedelta(days=i)
        stats.append({
            "date":      day.isoformat(),
            "label":     day.strftime("%a"),   # Mon, Tue …
            "completed": day in logged_dates,
        })
    return jsonify(stats), 200


# ─── Init ─────────────────────────────────────────────────────────────────────

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)