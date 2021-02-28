import psycopg2
import psycopg2.extras


DB_HOST = "db"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "1234"


def sendQuery(query):


    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            cur.execute(query)
            result = cur.fetchall()

    conn.close()
    return result

def addTask(task):


    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            cur.execute(task)

    conn.close()   

def deleteTask(id):


    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            cur.execute("DELETE FROM todolist.user_task WHERE user_task_id={};".format(id))

    conn.close() 


def updateTask(id, task):


    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            cur.execute("UPDATE todolist.user_task SET task='{}' WHERE user_task_id={};".format(task, id))

    conn.close()   