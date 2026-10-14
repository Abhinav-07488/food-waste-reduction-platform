import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "food_donation.db"


def connect_database():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def create_tables():

    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            donor_name TEXT,

            food_name TEXT,

            quantity INTEGER,

            location TEXT,

            expiry TEXT,

            status TEXT,

            matched_ngo TEXT
        )
    """)

    connection.commit()

    connection.close()