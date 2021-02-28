from flask import Flask, request, render_template, session, redirect, url_for, flash
import db
from models.UserModel import User
import sys

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def hello():
    if 'user_id' in session:
        return redirect(url_for("tasks"))
    return render_template("home.html",name="dmytro")

@app.route("/tasks")
def tasks():
    tasks = db.sendQuery("SELECT * FROM todolist.tasks;")
    return render_template("tasks.html", tasks=tasks)



# print([x for _, x in(db.sendQuery("SELECT * FROM todolist.users WHERE user_name LIKE '{}';".format("dmytro")))[0].items()], file=sys.stdout)
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        credentials = db.sendQuery("SELECT * FROM todolist.users WHERE user_name LIKE '{}';".format(username))
        if len(credentials) > 0:
            loginUser = User.from_dict(credentials[0])
            if loginUser.validate(username, password):
                session['user_id'] = credentials[0]['user_id']
                return redirect(url_for("tasks"))

        else:
            flash("Incorrect credentials!", "warning")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    if 'user_id' in session:
        flash("You've successfully logged out", "success")

    session.pop('user_id', None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')