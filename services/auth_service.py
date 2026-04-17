import bcrypt
import sqlite3
import os

class AuthService:
    def __init__(self, db_path="manager.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user'
                )
            ''')
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                self.create_user("admin", "admin123", "admin")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error initializing auth DB: {e}")

    def create_user(self, username, password, role="user"):
        try:
            pass_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                           (username, pass_hash, role))
            conn.commit()
            conn.close()
            return True, "Usuario creado con éxito."
        except sqlite3.IntegrityError:
            return False, "El usuario ya existe."
        except Exception as e:
            return False, str(e)

    def login(self, username, password):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                stored_hash = row[0].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    return True, {"username": username, "role": row[1]}
            return False, "Credenciales incorrectas."
        except Exception as e:
            return False, str(e)

    def list_users(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, role FROM users")
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception:
            return []

    def delete_user(self, username):
        if username == "admin": return False, "No se puede eliminar al admin principal."
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
            conn.close()
            return True, f"Usuario '{username}' eliminado."
        except Exception as e:
            return False, str(e)
