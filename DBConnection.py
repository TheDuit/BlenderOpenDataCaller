import psycopg2

def connect_to_db():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="112214",
        host="localhost",
        port="5432"
    )

    return conn, conn.cursor()
