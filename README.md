<div align="center">

# ✅ TaskFlow
### Smart Task Management System

![Python]
![Flask]
![PostgreSQL]
![WebSockets]
![Pandas]
![Numpy]

**A full-stack task management web application built with Flask, PostgreSQL, REST APIs, WebSockets, and real-time analytics using Pandas & NumPy.**

## 📌 Overview

TaskFlow is a productivity-focused web application that allows users to register, log in, and manage their tasks in real time. It features a clean dashboard with live WebSocket notifications, analytics powered by Pandas & NumPy, and a fully responsive UI built with HTML & CSS.


## 🚀 Features

| Feature | Description |
|---|---|
| 🔐 Authentication | Secure registration, login & logout with password hashing |
| 📝 Task Management | Add, update, delete, and view tasks with priority & status |
| 📊 Analytics Dashboard | Real-time stats — Total, Completed, Pending, Completion % |
| 📡 WebSocket Notifications | Live task notifications using Flask-SocketIO |
| 🗃️ PostgreSQL Database | Persistent storage with relational User & Task tables |
| 📱 Responsive UI | Clean, mobile-friendly interface with HTML & CSS |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | PostgreSQL, SQLAlchemy ORM |
| Real-Time | Flask-SocketIO, WebSockets |
| Analytics | Pandas, NumPy |
| Security | Werkzeug Password Hashing, Flask Sessions |
| Frontend | HTML5, CSS3, Font Awesome |

---

#  Video Demo

## 📂 Project Structure

```
flask_auth_app/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
│
├── templates/              # Jinja2 HTML templates
│   ├── home.html           # Landing page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   └── dashboard.html      # Main dashboard
│
└── static/
    └── style.css           # Custom CSS styles
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- PostgreSQL installed and running
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/flask_auth_app.git
cd flask_auth_app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL Database


### 4. Configure Database Connection

In `app.py`, update the connection string with your credentials:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:YOUR_PASSWORD@localhost:YOUR_PORT/flaskauth"
```

Example:
```python
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:admin123@localhost:5432/flaskauth"
```

### 5. Run the Application

```bash
python -m flask run
```

### 6. Open in Browser

```
http://127.0.0.1:5000
```

---

## 🔌 REST API Reference

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/` | No | Home page |
| GET/POST | `/register` | No | User registration |
| GET/POST | `/login` | No | User login |
| GET | `/logout` | Yes | Logout user |
| GET | `/dashboard` | Yes | Dashboard with analytics |
| POST | `/add-task` | Yes | Create a new task |
| GET | `/tasks` | Yes | Get all tasks (JSON) |
| POST | `/update-task/<id>` | Yes | Mark task as completed |
| POST | `/delete-task/<id>` | Yes | Delete a task |

---

## 🗄️ Database Schema

### Users Table
| Column | Type | Constraints |
|---|---|---|
| id | Integer | Primary Key |
| username | String(100) | Unique, Not Null |
| password | String(300) | Not Null (Hashed) |

### Tasks Table
| Column | Type | Constraints |
|---|---|---|
| id | Integer | Primary Key |
| title | String(200) | Not Null |
| description | String(500) | Not Null |
| priority | String(50) | Not Null (High/Medium/Low) |
| status | String(50) | Not Null (Pending/Completed) |
| created_date | DateTime | Default: UTC Now |
| user_id | Integer | Foreign Key → users.id |

---

## 📡 WebSocket Events

| Event | Direction | Description |
|---|---|---|
| `connect` | Server → Client | Sends welcome notification on connection |
| `task_notification` | Server → Client | Fires when a new task is added |

---

## 📊 Analytics Module

The dashboard analytics are computed using **Pandas** and **NumPy**:

```python
df = pd.DataFrame(task_data)
completed_tasks = np.sum(df["status"] == "Completed")
pending_tasks   = np.sum(df["status"] == "Pending")
completion_pct  = (completed_tasks / total_tasks) * 100
```

Metrics displayed:
- **Total Tasks** — all tasks for the logged-in user
- **Completed Tasks** — tasks with status "Completed"
- **Pending Tasks** — tasks with status "Pending"
- **Completion Percentage** — rounded to 2 decimal places

---

## 🔒 Security

- Passwords are hashed using **Werkzeug's** `generate_password_hash`
- Authentication is handled via **Flask sessions**
- All task routes are protected — unauthenticated users are redirected to login
- User tasks are isolated — each user only sees their own tasks

---

## ✅ Assignment Requirements Checklist

| Requirement | Marks | Status |
|---|---|---|
| Flask & REST APIs | 25 | ✅ Complete |
| PostgreSQL Integration | 20 | ✅ Complete |
| Code Quality | 20 | ✅ Complete |
| Pandas & NumPy Usage | 15 | ✅ Complete |
| WebSocket Feature | 10 | ✅ Complete |
| Frontend UI | 10 | ✅ Complete |
| **Total** | **100** | ✅ |



## 👩‍💻 Author

**Niharika Chauhan**
Python Development Internship — Sankar Group

