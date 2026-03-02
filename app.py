from flask import Flask, render_template, request, redirect, session
import sqlite3
from database import init_db

app = Flask(_name_)
app.secret_key = "supersecretkey"

init_db()

def get_db():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    if "admin" not in session:
        return redirect("/login")
    conn = get_db()
    attendance = conn.execute("SELECT * FROM attendance").fetchall()
    conn.close()
    return render_template("admin.html", attendance=attendance)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        admin = conn.execute("SELECT * FROM admin WHERE username=? AND password=?", 
                             (username, password)).fetchone()
        conn.close()

        if admin:
            session["admin"] = username
            return redirect("/")
        else:
            return "Invalid Login"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    date = request.form["date"]
    status = request.form["status"]

    conn = get_db()
    conn.execute("INSERT INTO attendance (name, date, status) VALUES (?, ?, ?)",
                 (name, date, status))
    conn.commit()
    conn.close()

    return redirect("/")

if _name_ == "_main_":

    app.run(debug=True)

