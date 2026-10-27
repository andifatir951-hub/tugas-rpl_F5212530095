import sqlite3
from pathlib import Path

class BukuModel:
    def __init__(self):
        # Simpan database di root proyek agar semua entry point memakai file yang sama.
        database_path = Path(__file__).resolve().parent.parent / "perpustakaan.db"
        self.conn = sqlite3.connect(database_path)
        # Mengatur agar hasil query bisa diakses seperti dictionary (buku['judul'])
        self.conn.row_factory = sqlite3.Row 
        self.buat_tabel()

    def buat_tabel(self):
        # Membuat tabel buku jika belum ada di database
        kursor = self.conn.cursor()
        kursor.execute('''
            CREATE TABLE IF NOT EXISTS buku (
                id_buku INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                penulis TEXT NOT NULL,
                tahun_terbit TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def get_all_buku(self):
        # Mengambil seluruh data buku dari database
        kursor = self.conn.cursor()
        kursor.execute("SELECT * FROM buku")
        return kursor.fetchall()

    def create_buku(self, judul, penulis, tahun):
        # Menyimpan data buku baru ke dalam database
        try:
            kursor = self.conn.cursor()
            kursor.execute('''
                INSERT INTO buku (judul, penulis, tahun_terbit) 
                VALUES (?, ?, ?)
            ''', (judul, penulis, tahun))
            self.conn.commit()
            return True # Sesuai dengan pengujian (assert hasil is True)
        except Exception as e:
            print(f"Error saat menyimpan: {e}")
            return False

    def update_buku(self, id_buku, judul, penulis, tahun):
        # Memperbarui data buku berdasarkan ID
        try:
            kursor = self.conn.cursor()
            kursor.execute('''
                UPDATE buku
                SET judul = ?, penulis = ?, tahun_terbit = ?
                WHERE id_buku = ?
            ''', (judul, penulis, tahun, id_buku))
            self.conn.commit()
            return kursor.rowcount > 0
        except Exception as e:
            print(f"Error saat memperbarui: {e}")
            return False

    def delete_buku(self, id_buku):
        # Menghapus data buku berdasarkan ID
        try:
            kursor = self.conn.cursor()
            kursor.execute("DELETE FROM buku WHERE id_buku = ?", (id_buku,))
            self.conn.commit()
            return kursor.rowcount > 0
        except Exception as e:
            print(f"Error saat menghapus: {e}")
            return False