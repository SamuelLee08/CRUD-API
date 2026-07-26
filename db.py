import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def init_db():
    """Create database and table if they don't exist."""
    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT false
        )
    """)
    
    # Count rows first
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    
    # Insert examples only when count is 0
    if count == 0:
        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (%s, %s)",
            ("Buy milk", False)
        )
        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (%s, %s)",
            ("Walk the dog", True)
        )
        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (%s, %s)",
            ("Study FastAPI", False)
        )
    
    conn.commit()
    cursor.close()
    conn.close()

def get_db_connection():
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    return conn

init_db()