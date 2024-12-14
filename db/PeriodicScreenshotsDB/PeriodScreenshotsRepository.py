from db_config import connection, cursor

class PeriodicScreenshotsRepository:
    def __init__(self):
        self.conn = connection
        self.cursor = cursor

    # Screenshots comes as a byte object already
    def insert_screenshot(self, screenshot, timestamp):
        query = "INSERT INTO PeriodicScreenshots (screenshot, timestamp) VALUES (?, ?)"
        self.cursor.execute(query, (screenshot, timestamp))
        self.conn.commit()
        return True