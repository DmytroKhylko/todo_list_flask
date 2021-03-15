from flask import Flask, request, render_template, session, redirect, url_for, flash, g
import db
import sys
import hashlib
import functools
import bcrypt
from models.UserModel import User

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def login_required(func):
    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if 'user_id' not in session:
            flash("Log in, please, to access your tasks", "is-danger")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper_login_required

@app.before_request
def before_request():
    g.db = db.get_db()
    if 'user_id' in session:
        g.user = User.getUserById(session['user_id'])


@app.route("/")
def home():
    if 'user_id' in session:
        return render_template("home.html",name=g.user.name)
    return render_template("home.html", name=None)



@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        if not db.userExists(username):
            db.addUser(username, password)
            session.pop('user_id', None)
            user = User.getUserByName(username)
            session['user_id'] = user.id
            g.user = user
            return redirect(url_for("tasks"))

        flash("Username not avaliable", "is-warning")
        return redirect(url_for("signup"))

    return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username'].strip()
        password = request.form['password']

        loginUser = User.getUserByName(username)
        if loginUser != None and loginUser.validate(username, password):
            session['user_id'] = loginUser.id
            g.user = loginUser
            return redirect(url_for("tasks"))


        flash("Incorrect credentials!", "is-warning")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/tasks", methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        task = request.form['content']
        g.user.addTask(task)
        tasks = g.user.getTasks()
        return render_template("tasks.html", name=g.user.name, tasks=tasks)
    tasks = g.user.getTasks()
    return render_template("tasks.html", name=g.user.name, tasks=tasks)



@app.route("/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update(id):
    task = g.user.getTask(id)
    if request.method == 'POST':
        updated_task = request.form['content']
        g.user.updateTask(id, updated_task)
        return redirect(url_for("tasks"))
    return render_template('update.html',task=task[0])
    
@app.route("/delete/<int:id>")
@login_required
def delete(id):
    g.user.deleteTask(id)
    return redirect(url_for("tasks"))

@app.route("/logout")
def logout():
    if 'user_id' in session:
        flash("You've successfully logged out", "is-success")

    session.pop('user_id', None)
    g.user = None
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')