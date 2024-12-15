import sqlite3
from db_config import CONNECTION_URL
conn = sqlite3.connect(CONNECTION_URL)
cursor = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS ActiveWindows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    start_time DATETIME,
    duration INTEGER -- in seconds
);"""

cursor.execute(query)
conn.commit()
print("ActiveWindows table initialized")
conn.close()