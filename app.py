from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///habits.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)