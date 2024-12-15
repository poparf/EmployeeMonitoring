import sqlite3
from db.db_config import CONNECTION_URL

class WindowTrackerRepository:
    def __init__(self):
        self.conn = sqlite3.connect(CONNECTION_URL)
        self.cursor = self.conn.cursor()

    """
    params: data - tuple of (title Text,
                            start_time Datetime,
                            duration Integer) 
    """
    def insert(self, data):
        self.cursor.execute("INSERT INTO ActiveWindows VALUES (?, ?, ?)", data)
        self.conn.commit()

    def select(self):
        self.cursor.execute("SELECT * FROM ActiveWindows")
        return self.cursor.fetchall()

    def select_from_id_to_last(self, id):
        self.cursor.execute("SELECT * FROM ActiveWindows WHERE id > ?", (id,))
        return self.cursor.fetchall()

    def delete_from_id_to_first(self, id):
        self.cursor.execute("DELETE FROM ActiveWindows WHERE id < ?", (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()