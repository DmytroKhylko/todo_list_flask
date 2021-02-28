import psycopg2
import psycopg2.extras

def sendQuery(query):
    DB_HOST = "db"
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASS = "1234"

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            cur.execute(query)
            result = cur.fetchall()

    conn.close()
    return result