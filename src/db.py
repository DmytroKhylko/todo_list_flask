from flask import g, Flask
import psycopg2
import psycopg2.extras
import hashlib
import sys
import bcrypt



DB_HOST = "db"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "1234"


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def getUserFromDbById(user_id):
    with g.db:
        with g.db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM todolist.users WHERE user_id = %s;",(user_id,))
            result = cur.fetchall()
            if len(result) == 0:
                return None
    return result[0]


def getUserFromDbByName(username):
    with g.db:
        with g.db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM todolist.users WHERE user_name = %s;",(username,))
            result = cur.fetchall()
            if len(result) == 0:
                return None
    return result[0]


def userExists(username):
    with g.db:
        with g.db.cursor() as cur:
            cur.execute("SELECT user_name FROM todolist.users WHERE user_name LIKE %s;",(username,))
            result = cur.fetchall()
    return len(result) != 0

def addUser(username, password):
    with g.db:
        with g.db.cursor() as cur:
            salt = bcrypt.gensalt()
            hashed_passwd = bcrypt.hashpw(password.encode('utf-8'), salt)
            cur.execute("INSERT INTO todolist.users (user_name,user_password) VALUES (%s, %s)",(username, hashed_passwd.decode('utf-8')))



def addTaskDb(user_id, task):
    with g.db:
        with g.db.cursor() as cur:
            cur.execute("INSERT INTO todolist.user_task (user_id, task) VALUES (%s, %s);",(user_id, task))

def getTasksDb(user_id):
    with g.db:
        with g.db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM todolist.user_task WHERE user_id = %s;",(user_id,))
            result = cur.fetchall()
    return result

def getTaskDb(user_task_id):
    with g.db:
        with g.db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM todolist.user_task WHERE user_task_id = %s;", (user_task_id,))
            result = cur.fetchall()
    return result

def updateTaskDb(id, task):
    with g.db:
        with g.db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            cur.execute("UPDATE todolist.user_task SET task=%s WHERE user_task_id=%s;",(task, id))

def deleteTaskDb(id):
    with g.db:
        with g.db.cursor() as cur:
            cur.execute("DELETE FROM todolist.user_task WHERE user_task_id=%s;",(id,))






