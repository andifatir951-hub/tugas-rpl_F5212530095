from unittest.mock import MagicMock

from controllers.auth_controller import AuthController
from models.user_model import UserModel


def test_login_berhasil_mengembalikan_role_dan_menutup_tampilan():
    controller = AuthController.__new__(AuthController)
    controller.model = MagicMock()
    controller.view = MagicMock()
    controller.role = None
    controller.run_application = False

    controller.buka_aplikasi("anggota")

    assert controller.role == "anggota"
    controller.model.close.assert_called_once()
    controller.view.quit.assert_called_once()
    controller.view.destroy.assert_called_once()


def test_hash_password_konsisten():
    password_asli = "admin123"
    hash_1 = UserModel.hash_password(password_asli)
    hash_2 = UserModel.hash_password(password_asli)

    # Memastikan hasil hash tidak sama dengan plain text dan bersifat konsisten
    assert hash_1 != password_asli
    assert hash_1 == hash_2
    assert len(hash_1) == 64 # Panjang karakter standar SHA-256

def test_autentikasi_pengguna_berhasil():
    model = UserModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()

    # Simulasi kembalian data dari database ketika username & password cocok
    mock_cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "petugas",
        "role": "admin"
    }
    model.conn.cursor.return_value = mock_cursor

    hasil = model.autentikasi("petugas", "admin123")

    assert hasil is not None
    assert hasil["username"] == "petugas"
    assert hasil["role"] == "admin"