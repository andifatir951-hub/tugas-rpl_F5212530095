from models.user_model import UserModel


def test_autentikasi_berhasil(tmp_path):
    model = UserModel(tmp_path / "perpustakaan.db")

    try:
        assert model.buat_admin_pertama("petugas", "rahasia")

        user = model.autentikasi("petugas", "rahasia")

        assert user is not None
        assert tuple(user) == (1, "petugas", "admin")
    finally:
        model.close()


def test_autentikasi_gagal_untuk_password_salah(tmp_path):
    model = UserModel(tmp_path / "perpustakaan.db")

    try:
        assert model.buat_admin_pertama("petugas", "rahasia")

        assert model.autentikasi("petugas", "salah") is None
    finally:
        model.close()


def test_autentikasi_menggunakan_parameter_query(tmp_path):
    model = UserModel(tmp_path / "perpustakaan.db")

    try:
        assert model.autentikasi("' OR 1=1 --", "apa saja") is None
    finally:
        model.close()


def test_admin_hanya_dapat_dibuat_jika_belum_ada_pengguna(tmp_path):
    model = UserModel(tmp_path / "perpustakaan.db")

    try:
        assert model.belum_ada_pengguna()
        assert not model.buat_admin_pertama("", "rahasia")
        assert model.buat_admin_pertama("petugas", "rahasia")
        assert not model.belum_ada_pengguna()
        assert not model.buat_admin_pertama("lainnya", "rahasia")
    finally:
        model.close()
