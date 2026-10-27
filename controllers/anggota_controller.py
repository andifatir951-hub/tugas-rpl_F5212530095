import tkinter.messagebox as messagebox

from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView


class AnggotaController:
    def __init__(self):
        self.model = AnggotaModel()
        self.view = AnggotaView()
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.perbarui_data)
        self.view.btn_delete.configure(command=self.hapus_data)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_data)
        self.view.protocol("WM_DELETE_WINDOW", self.tutup)
        self.id_anggota_terpilih = None
        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        for anggota in self.model.get_all_anggota():
            self.view.tabel.insert(
                "",
                "end",
                values=(anggota["id_anggota"], anggota["nama"], anggota["alamat"]),
            )

    def pilih_data(self, _event=None):
        pilihan = self.view.tabel.selection()
        if not pilihan:
            self.id_anggota_terpilih = None
            return

        nilai = self.view.tabel.item(pilihan[0], "values")
        self.id_anggota_terpilih = nilai[0]
        self.view.entry_nama.delete(0, "end")
        self.view.entry_nama.insert(0, nilai[1])
        self.view.entry_alamat.delete(0, "end")
        self.view.entry_alamat.insert(0, nilai[2])

    def bersihkan_form(self):
        self.view.entry_nama.delete(0, "end")
        self.view.entry_alamat.delete(0, "end")
        self.id_anggota_terpilih = None
        pilihan = self.view.tabel.selection()
        if pilihan:
            self.view.tabel.selection_remove(*pilihan)

    def simpan_data(self):
        nama = self.view.entry_nama.get().strip()
        alamat = self.view.entry_alamat.get().strip()

        if not nama or not alamat:
            messagebox.showwarning(
                "Peringatan",
                "Nama dan alamat anggota harus diisi!",
                parent=self.view,
            )
            return

        if not self.model.create_anggota(nama, alamat):
            messagebox.showerror(
                "Error",
                "Terjadi kesalahan saat menyimpan data anggota.",
                parent=self.view,
            )
            return

        messagebox.showinfo(
            "Sukses",
            "Data anggota berhasil disimpan!",
            parent=self.view,
        )
        self.bersihkan_form()
        self.muat_data_tabel()

    def perbarui_data(self):
        if self.id_anggota_terpilih is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih anggota yang ingin diperbarui!",
                parent=self.view,
            )
            return

        nama = self.view.entry_nama.get().strip()
        alamat = self.view.entry_alamat.get().strip()
        if not nama or not alamat:
            messagebox.showwarning(
                "Peringatan",
                "Nama dan alamat anggota harus diisi!",
                parent=self.view,
            )
            return

        if not self.model.update_anggota(
            self.id_anggota_terpilih, nama, alamat
        ):
            messagebox.showerror(
                "Error",
                "Terjadi kesalahan saat memperbarui data anggota.",
                parent=self.view,
            )
            return

        messagebox.showinfo(
            "Sukses",
            "Data anggota berhasil diperbarui!",
            parent=self.view,
        )
        self.bersihkan_form()
        self.muat_data_tabel()

    def hapus_data(self):
        if self.id_anggota_terpilih is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih anggota yang ingin dihapus!",
                parent=self.view,
            )
            return

        if not messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus data anggota yang dipilih?",
            parent=self.view,
        ):
            return

        if not self.model.delete_anggota(self.id_anggota_terpilih):
            messagebox.showerror(
                "Error",
                "Terjadi kesalahan saat menghapus data anggota.",
                parent=self.view,
            )
            return

        messagebox.showinfo(
            "Sukses",
            "Data anggota berhasil dihapus!",
            parent=self.view,
        )
        self.bersihkan_form()
        self.muat_data_tabel()

    def tutup(self):
        self.model.close()
        self.view.destroy()

    def run(self):
        self.view.mainloop()
