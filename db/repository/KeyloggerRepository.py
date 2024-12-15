from ..db_config import connection,cursor

class KeyloggerRepository:
    def __init__(self):
        self.conn = connection
        self.cursor = cursor
        
    def insert_keylog(self, keys, start_time, end_time):
        query = "INSERT INTO Keylogger (keys, start_time, end_time) VALUES (?, ?, ?)"
        self.cursor.execute(query, (keys, start_time, end_time))
        self.conn.commit()
        return True
    
    def close(self):
        self.conn.close()