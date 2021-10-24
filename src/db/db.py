import os , psycopg2

pg_host = os.environ.get('PG_HOST', "127.0.0.1")
pg_port = os.environ.get('PG_PORT', "5432")
pg_user = os.environ.get('PG_USER', "postgres")
pg_password = os.environ.get('PG_PASSWORD', "somePassword")
pg_db = os.environ.get('PG_DB', "postgres")

DSN = ("dbname=" + pg_db + " user=" + pg_user + " password=" + pg_password + " host=" + pg_host + " port=" + pg_port)

def get_dob(user):
    SQL = "SELECT birth_date FROM birthdays WHERE username = %s"
    with psycopg2.connect(DSN) as conn:
        with conn.cursor() as curs:
            curs.execute(SQL, (user,))
            return curs.fetchall()

def upsert_dob(user,dob):
    SQL = """INSERT INTO birthdays (username, birth_date) 
            VALUES(%s, %s) 
            ON CONFLICT (username) 
            DO 
            UPDATE SET birth_date = %s"""
    with psycopg2.connect(DSN) as conn:
        with conn.cursor() as curs:
            curs.execute(SQL, (user,dob,dob))


