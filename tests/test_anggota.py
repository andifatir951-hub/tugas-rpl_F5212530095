from unittest.mock import MagicMock

from controllers.anggota_controller import AnggotaController
from models.anggota_model import AnggotaModel


def test_logout_anggota_membuka_halaman_login(monkeypatch):
    controller = AnggotaController.__new__(AnggotaController)
    controller.model = MagicMock()
    controller.view = MagicMock()
    auth_controller = MagicMock()
    monkeypatch.setattr(
        "controllers.auth_controller.AuthController",
        MagicMock(return_value=auth_controller),
    )

    controller.logout()

    controller.model.close.assert_called_once()
    controller.view.destroy.assert_called_once()
    auth_controller.run.assert_called_once()


def test_anggota_tersimpan_dan_dapat_dibaca(tmp_path):
    model = AnggotaModel(tmp_path / "perpustakaan.db")

    try:
        assert model.create_anggota("Ayu", "Jalan Melati")

        anggota = model.get_all_anggota()

        assert len(anggota) == 1
        assert tuple(anggota[0]) == (1, "Ayu", "Jalan Melati")
    finally:
        model.close()


def test_anggota_dapat_diperbarui(tmp_path):
    model = AnggotaModel(tmp_path / "perpustakaan.db")

    try:
        assert model.create_anggota("Ayu", "Jalan Melati")
        id_anggota = model.get_all_anggota()[0]["id_anggota"]

        assert model.update_anggota(id_anggota, "Budi", "Jalan Mawar")
        anggota = model.get_all_anggota()[0]

        assert tuple(anggota) == (id_anggota, "Budi", "Jalan Mawar")
    finally:
        model.close()


def test_anggota_dapat_dihapus(tmp_path):
    model = AnggotaModel(tmp_path / "perpustakaan.db")

    try:
        assert model.create_anggota("Ayu", "Jalan Melati")
        id_anggota = model.get_all_anggota()[0]["id_anggota"]

        assert model.delete_anggota(id_anggota)
        assert model.get_all_anggota() == []
        assert not model.delete_anggota(id_anggota)
    finally:
        model.close()
