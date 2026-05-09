from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit
from datetime import datetime
import pandas as pd
import numpy as np

app = Flask(__name__)


app.secret_key = "supersecretkey"


# POSTGRESQL CONNECTION
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Neha123%40@localhost:5711/flaskauth"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

socketio = SocketIO(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(300),
        nullable=False
    )

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.String(500),
        nullable=False
    )

    priority = db.Column(
        db.String(50),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False
    )

    created_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )


# CREATE DATABASE TABLES
with app.app_context():
    db.create_all()


# HOME PAGE
@app.route("/")
def home():

    return render_template("home.html")


# REGISTER

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        # CHECK IF USER EXISTS
        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            return "Username already exists"

        
        hashed_password = generate_password_hash(password)

        
        new_user = User(
            username=username,
            password=hashed_password
        )

        # SAVE TO DATABASE
        db.session.add(new_user)

        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        # FIND USER
        user = User.query.filter_by(
            username=username
        ).first()

        # VERIFY PASSWORD
        if user and check_password_hash(
            user.password,
            password
        ):

            # CREATE SESSION
            session["user"] = username

            session["user_id"] = user.id

            return redirect("/dashboard")

        else:

            return "Invalid Credentials"

    return render_template("login.html")

# DASHBOARD

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect("/login")


    tasks = Task.query.filter_by(
        user_id=session["user_id"]
    ).all()

   
    # ANALYTICS USING PANDAS

    task_data = []

    for task in tasks:

        task_data.append({
            "status": task.status
        })

    df = pd.DataFrame(task_data)

    total_tasks = len(df)

    completed_tasks = 0

    pending_tasks = 0

    completion_percentage = 0

    if total_tasks > 0:

        completed_tasks = np.sum(
            df["status"] == "Completed"
        )

        pending_tasks = np.sum(
            df["status"] == "Pending"
        )

        completion_percentage = (
            completed_tasks / total_tasks
        ) * 100

    return render_template(
        "dashboard.html",
        username=session["user"],
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        completion_percentage=round(
            completion_percentage,
            2
        )
    )


# ADD TASK
@app.route("/add-task", methods=["POST"])
def add_task():

    if "user" not in session:

        return redirect("/login")

    title = request.form["title"]

    description = request.form["description"]

    priority = request.form["priority"]

    status = request.form["status"]

    # CREATE TASK OBJECT
    new_task = Task(
        title=title,
        description=description,
        priority=priority,
        status=status,
        user_id=session["user_id"]
    )

    # SAVE TASK
    db.session.add(new_task)

    db.session.commit()

    # WEBSOCKET NOTIFICATION
    socketio.emit(
        "task_notification",
        {
            "message": f"New Task Added: {title}"
        }
    )

    return redirect("/dashboard")


# GET ALL TASKS API

@app.route("/tasks", methods=["GET"])
def get_tasks():

    tasks = Task.query.filter_by(
        user_id=session["user_id"]
    ).all()

    task_list = []

    for task in tasks:

        task_list.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "created_date": str(task.created_date)
        })

    return jsonify(task_list)

# UPDATE TASK
@app.route("/update-task/<int:id>", methods=["POST"])
def update_task(id):

    task = Task.query.get(id)

    if task:

        task.status = "Completed"

        db.session.commit()

    return redirect("/dashboard")


# DELETE TASK
@app.route("/delete-task/<int:id>", methods=["POST"])
def delete_task(id):

    task = Task.query.get(id)

    if task:

        db.session.delete(task)

        db.session.commit()

    return redirect("/dashboard")


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("user", None)

    session.pop("user_id", None)

    return redirect("/login")


@socketio.on("connect")
def handle_connect():

    emit(
        "task_notification",
        {
            "message": "Connected to WebSocket Server"
        }
    )

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)