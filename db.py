import sqlite3

DATABASE = "tasks.db"

def init_db():
    """Create database and table if they don't exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    
    # Count rows first
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    
    # Insert examples only when count is 0
    if count == 0:
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Buy milk", 0))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Walk the dog", 1))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Study FastAPI", 0))
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

init_db()