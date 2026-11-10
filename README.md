# Aplikasi Sistem Perpustakaan

Aplikasi desktop untuk mengelola buku dan anggota perpustakaan, dengan autentikasi pengguna dan hak akses berdasarkan peran. Antarmuka dibuat menggunakan CustomTkinter dan data disimpan di SQLite.

## Struktur Direktori (MVC)

```text
.
├── controllers/       # Logika aplikasi dan penghubung model dengan view
├── models/            # Akses data buku, anggota, dan pengguna
├── views/             # Antarmuka login, buku, dan anggota
├── tests/             # Automated tests menggunakan pytest
├── .github/workflows/ # Pipeline CI GitHub Actions
├── main.py            # Entry point aplikasi
├── perpustakaan.db    # Database SQLite (dibuat saat aplikasi dijalankan)
└── requirements.txt   # Dependensi Python
```

## Instalasi dan Database

1. Pastikan Python 3.11 atau lebih baru telah terpasang.
2. Buat dan aktifkan virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Pasang dependensi:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Database saat ini menggunakan **SQLite**, bukan MySQL. Tidak diperlukan server atau konfigurasi database terpisah. Aplikasi membuat atau membuka `perpustakaan.db` di direktori root proyek saat dijalankan.

## Menjalankan Aplikasi

Dari direktori root proyek, jalankan:

```powershell
python main.py
```

Untuk menjalankan pengujian dan pemeriksaan linter:

```powershell
pytest -v
flake8 models/ controllers/ --count --select=E9,F63,F7,F82 --show-source --statistics
```
