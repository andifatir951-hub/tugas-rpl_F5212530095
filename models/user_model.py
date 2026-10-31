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
        cursor.executemany(
            "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
            (
                ("petugas", self.hash_password("admin123"), "admin"),
                ("mahasiswa", self.hash_password("user123"), "anggota"),
            ),
        )
        self.conn.commit()

    def register_user(self, username, password, role):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, self.hash_password(password), role),
            )
            self.conn.commit()
            return True
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
