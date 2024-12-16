import sqlite3
from db.db_config import CONNECTION_URL

class PeriodicScreenshotsRepository:
    def __init__(self):
        # We need to reestablish ocnnection since sqlite is not thread safe
        self.conn = sqlite3.connect(CONNECTION_URL, check_same_thread=False)
        self.cursor = self.conn.cursor()

    # Screenshots comes as a byte object already
    def insert_screenshot(self, screenshot, timestamp):
        query = "INSERT INTO PeriodicScreenshots (screenshot, timestamp) VALUES (?, ?)"
        self.cursor.execute(query, (screenshot, timestamp))
        self.conn.commit()
        return True

    def close(self):
        self.conn.close()