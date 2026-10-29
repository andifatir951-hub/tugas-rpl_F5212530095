import hashlib
import sqlite3
from pathlib import Path


class UserModel:
    def __init__(self, database_path=None):
        if database_path is None:
            database_path = Path(__file__).resolve().parent.parent / "perpustakaan.db"
        self.conn = sqlite3.connect(database_path)
        self.conn.row_factory = sqlite3.Row
        self.buat_tabel()

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def buat_tabel(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def belum_ada_pengguna(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT 1 FROM users LIMIT 1")
            return cursor.fetchone() is None
        finally:
            cursor.close()

    def buat_admin_pertama(self, username, password):
        if not username or not password:
            return False

        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) "
                "SELECT ?, ?, 'admin' WHERE NOT EXISTS "
                "(SELECT 1 FROM users)",
                (username, self.hash_password(password)),
            )
            self.conn.commit()
            return cursor.rowcount == 1
        finally:
            cursor.close()

    def autentikasi(self, username, password):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "SELECT id_user, username, role FROM users "
                "WHERE username = ? AND password = ?",
                (username, self.hash_password(password)),
            )
            return cursor.fetchone()
        finally:
            cursor.close()

    def close(self):
        self.conn.close()
