import time
import sqlite3
import os

class MonitorService:
    def __init__(self, logs_dir="logs"):
        self.logs_dir = logs_dir
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        self.db_path = os.path.join(logs_dir, "monitor.db")
        self._init_db()

    def _init_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user TEXT,
                    operation TEXT,
                    table_name TEXT,
                    duration REAL,
                    status TEXT,
                    details TEXT
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"MonitorService: Error initializing DB: {e}")

    def log_activity(self, user, operation, table_name="", duration=0.0, status="Success", details=""):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO activity_log (user, operation, table_name, duration, status, details) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user, operation, table_name, duration, status, details))
            conn.commit()
            conn.close()
        except Exception:
            pass

    def get_logs(self, limit=100):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, user, operation, status, duration FROM activity_log ORDER BY timestamp DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception:
            return []

    def get_user_stats(self, user):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM activity_log WHERE user = ?", (user,))
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception:
            return 0
