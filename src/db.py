import sqlite3
from typing import List, Tuple

class ChatHistoryDatabase:
    def __init__(self, db_name: str = 'src/chat_history.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    user_id INTEGER,
                    role TEXT,
                    message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def add_message(self, user_id: int, role: str, message: str):
        with self.conn:
            self.conn.execute("""
                INSERT INTO history (user_id, role, message) VALUES (?, ?, ?)
            """, (user_id, role, message))

    def get_history(self, user_id: int, limit: int = 100) -> List[Tuple[str, str]]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT role, message FROM history 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (user_id, limit))
        return cursor.fetchall()

    def clear_history(self, user_id: int):
        with self.conn:
            self.conn.execute("""
                DELETE FROM history WHERE user_id = ?
            """, (user_id,))

    def close(self):
        self.conn.close()
