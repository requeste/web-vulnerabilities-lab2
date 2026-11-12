import sqlite3
from pathlib import Path

db_path = Path(__file__).with_name("database.db")

def db_init():
    db = sqlite3.connect(db_path)

    db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    db.commit
    db.close()

def add_user(username, password):
    db = sqlite3.connect(db_path)

    try:
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password)
        )
        db.commit()

    finally:
        db.close()

def check_user(username, password):
    db = sqlite3.connect(db_path)

    try:
        query = (
            "SELECT * FROM users "
            f"WHERE username = '{username}' AND password_hash = '{password}'"
        )

        user = db.execute(query).fetchone()

        return user is not None 
        
    finally:
        db.close()


