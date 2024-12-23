import sqlite3
from db_config import CONNECTION_URL
conn = sqlite3.connect(CONNECTION_URL)
cursor = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS Keylogger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time DATETIME,
    keys TEXT,
    end_time DATETIME
);
"""
cursor.execute(query)
conn.commit()
print("Keylogger table initialized")
conn.close()
