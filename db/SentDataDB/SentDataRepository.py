from db_config import connection, cursor

class SentDataRepository:
    def __init__(self):
        self.conn = connection
        self.cursor = cursor

    def get_last_synced_id(self, table_name):
        query = f"SELECT last_synced_id FROM {self.table_name} WHERE table_name = ?"
        self.cursor.execute(query, (table_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def set_last_synced_id(self, table_name, last_synced_id):
        query = f"INSERT OR REPLACE INTO {self.table_name} (table_name, last_synced_id) VALUES (?, ?)"
        self.cursor.execute(query, (table_name, last_synced_id))
        self.conn.commit()
        return True

