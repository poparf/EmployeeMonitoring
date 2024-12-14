import sqlite3
from db_config import CONNECTION_URL
conn = sqlite3.connect(CONNECTION_URL)
cursor = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS PeriodicScreenshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    screenshot BLOB,
    timestamp DATETIME
);
"""
cursor.execute(query)
conn.commit()
print("PeriodicScreenshots table initialized")
conn.close()