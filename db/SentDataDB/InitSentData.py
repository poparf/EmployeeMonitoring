import sqlite3
from db_config import CONNECTION_URL

conn = sqlite3.connect(CONNECTION_URL)
cursor = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS SentData (
    table_name TEXT PRIMARY KEY,
    last_synced_id INTEGER   
);
"""
cursor.execute(query)
conn.commit()
print("SentData table initialized")
conn.close()