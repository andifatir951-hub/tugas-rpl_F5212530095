import sqlite3

class BukuModel:
    def __init__(self):
        # Membuat koneksi ke database SQLite (akan otomatis membuat file perpustakaan.db jika belum ada)
        self.conn = sqlite3.connect("perpustakaan.db")
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