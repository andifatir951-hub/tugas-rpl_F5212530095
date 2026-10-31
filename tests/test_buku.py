from unittest.mock import MagicMock
from controllers import buku_controller
from controllers.buku_controller import BukuController
from models.buku_model import BukuModel


def test_anggota_ditolak_saat_memperbarui_buku(monkeypatch):
    controller = BukuController.__new__(BukuController)
    controller.user_role = "anggota"
    showerror = MagicMock()
    monkeypatch.setattr(buku_controller.messagebox, "showerror", showerror)

    controller.perbarui_data()

    showerror.assert_called_once()


def test_anggota_ditolak_saat_menghapus_buku(monkeypatch):
    controller = BukuController.__new__(BukuController)
    controller.user_role = "anggota"
    showerror = MagicMock()
    monkeypatch.setattr(buku_controller.messagebox, "showerror", showerror)

    controller.hapus_data()

    showerror.assert_called_once()


def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()
    
    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor
    
    # Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)
    
    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True
    # Memverifikasi apakah cursor.execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()
    # Memverifikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()

def test_update_buku_berhasil():
    model = BukuModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 1
    model.conn.cursor.return_value = mock_cursor

    hasil = model.update_buku(1, "Buku Baru", "Penulis Baru", 2026)

    assert hasil is True
    mock_cursor.execute.assert_called_once_with(
        "\n                UPDATE buku\n"
        "                SET judul = ?, penulis = ?, tahun_terbit = ?\n"
        "                WHERE id_buku = ?\n            ",
        ("Buku Baru", "Penulis Baru", 2026, 1),
    )
    model.conn.commit.assert_called_once()

def test_delete_buku_berhasil():
    model = BukuModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 1
    model.conn.cursor.return_value = mock_cursor

    hasil = model.delete_buku(1)

    assert hasil is True
    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM buku WHERE id_buku = ?", (1,)
    )
    model.conn.commit.assert_called_once()