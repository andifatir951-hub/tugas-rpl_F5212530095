import sqlite3
from pathlib import Path


class AnggotaModel:
    def __init__(self, database_path=None):
        if database_path is None:
            database_path = Path(__file__).resolve().parent.parent / "perpustakaan.db"
        self.conn = sqlite3.connect(database_path)
        self.conn.row_factory = sqlite3.Row
        self.buat_tabel()

    def buat_tabel(self):
        kursor = self.conn.cursor()
        kursor.execute("""
            CREATE TABLE IF NOT EXISTS anggota (
                id_anggota INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                alamat TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def get_all_anggota(self):
        kursor = self.conn.cursor()
        kursor.execute(
            "SELECT id_anggota, nama, alamat FROM anggota ORDER BY id_anggota"
        )
        return kursor.fetchall()

    def create_anggota(self, nama, alamat):
        try:
            kursor = self.conn.cursor()
            kursor.execute(
                "INSERT INTO anggota (nama, alamat) VALUES (?, ?)",
                (nama, alamat),
            )
            self.conn.commit()
            return True
        except sqlite3.Error as error:
            print(f"Error saat menyimpan anggota: {error}")
            return False

    def update_anggota(self, id_anggota, nama, alamat):
        try:
            kursor = self.conn.cursor()
            kursor.execute(
                "UPDATE anggota SET nama = ?, alamat = ? WHERE id_anggota = ?",
                (nama, alamat, id_anggota),
            )
            self.conn.commit()
            return kursor.rowcount > 0
        except sqlite3.Error as error:
            print(f"Error saat memperbarui anggota: {error}")
            return False

    def delete_anggota(self, id_anggota):
        try:
            kursor = self.conn.cursor()
            kursor.execute(
                "DELETE FROM anggota WHERE id_anggota = ?",
                (id_anggota,),
            )
            self.conn.commit()
            return kursor.rowcount > 0
        except sqlite3.Error as error:
            print(f"Error saat menghapus anggota: {error}")
            return False

    def close(self):
        self.conn.close()
