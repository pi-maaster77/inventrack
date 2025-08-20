import sqlite3

DB_PATH = "db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def commit():
    conn.commit()

def close():
    conn.close()
