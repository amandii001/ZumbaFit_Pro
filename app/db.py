import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",         # XAMPP default
            password="",         # change if you set root password
            database="zumbafitpro"
        )
        return conn
    except Error as e:
        print("❌ DB Connection Error:", e)
        return None

def close_connection(conn, cursor=None):
    """Safely close database connections"""
    if cursor:
        cursor.close()
    if conn:
        conn.close()
