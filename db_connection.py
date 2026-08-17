import pymysql

def get_db_connection():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="fintech_users",
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn
