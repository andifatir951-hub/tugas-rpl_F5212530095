import sqlite3

from models.user_model import UserModel


def test_autentikasi_berhasil(tmp_path):
    model = UserModel(tmp_path / "perpustakaan.db")

    try:
        user = model.autentikasi("petugas", "admin123")

        assert user is not None
        assert tuple(user) == (1, "petugas", "admin")
    finally:
        model.close()


def test_autentikasi_anggota_default(tmp_path):
    model = UserModel(tmp_path / "perpustakaan.db")

    try:
        user = model.autentikasi("mahasiswa", "user123")

        assert user is not None
        assert tuple(user) == (2, "mahasiswa", "anggota")
    finally:
        model.close()


def test_autentikasi_gagal_untuk_password_salah(tmp_path):
    model = UserModel(tmp_path / "perpustakaan.db")

    try:
        assert model.autentikasi("petugas", "salah") is None
    finally:
        model.close()


def test_register_user_menyimpan_password_dalam_hash_sha256(tmp_path):
    model = UserModel(tmp_path / "perpustakaan.db")

    try:
        assert model.register_user("pengguna_baru", "kata-sandi", "anggota") is True

        user = model.conn.execute(
            "SELECT username, password, role FROM users WHERE username = ?",
            ("pengguna_baru",),
        ).fetchone()

        assert tuple(user) == (
            "pengguna_baru",
            UserModel.hash_password("kata-sandi"),
            "anggota",
        )
        assert model.autentikasi("pengguna_baru", "kata-sandi") is not None
    finally:
        model.close()


def test_autentikasi_menggunakan_parameter_query(tmp_path):
    model = UserModel(tmp_path / "perpustakaan.db")

    try:
        assert model.autentikasi("' OR 1=1 --", "apa saja") is None
    finally:
        model.close()


def test_akun_default_ditambahkan_tanpa_mengubah_akun_lama(tmp_path):
    database_path = tmp_path / "perpustakaan.db"
    connection = sqlite3.connect(database_path)
    connection.execute("""
        CREATE TABLE users (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    connection.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ("tihur", UserModel.hash_password("password-lama"), "admin"),
    )
    connection.commit()
    connection.close()

    model = UserModel(database_path)

    try:
        assert model.autentikasi("tihur", "password-lama") is not None
        assert model.autentikasi("petugas", "admin123") is not None
        assert model.autentikasi("mahasiswa", "user123") is not None
    finally:
        model.close()
