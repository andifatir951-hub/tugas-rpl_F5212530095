import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()
        self.id_buku_terpilih = None

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Binding tombol aksi
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.perbarui_data)
        self.view.btn_delete.configure(command=self.hapus_data)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_data)

        # Hanya admin yang dapat mengubah koleksi buku.
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_update.configure(
                state="disabled", text="Perbarui Data (Khusus Admin)"
            )
            self.view.btn_delete.configure(
                state="disabled", text="Hapus Data (Khusus Admin)"
            )
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    def pilih_data(self, _event=None):
        pilihan = self.view.tabel.selection()
        if not pilihan:
            self.id_buku_terpilih = None
            return

        nilai = self.view.tabel.item(pilihan[0], "values")
        self.id_buku_terpilih = nilai[0]
        for entry, value in zip(
            (self.view.entry_judul, self.view.entry_penulis, self.view.entry_tahun),
            nilai[1:],
        ):
            entry.configure(state="normal")
            entry.delete(0, "end")
            entry.insert(0, value)
            if self.user_role != "admin":
                entry.configure(state="disabled")

    def simpan_data(self):
        # Proteksi ganda di level controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    def perbarui_data(self):
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Hanya admin yang dapat mengubah data buku.")
            return
        if self.id_buku_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin diperbarui!")
            return

        data = (
            self.view.entry_judul.get(),
            self.view.entry_penulis.get(),
            self.view.entry_tahun.get(),
        )
        if not all(data):
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if self.model.update_buku(self.id_buku_terpilih, *data):
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal memperbarui data.")

    def hapus_data(self):
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Hanya admin yang dapat menghapus data buku.")
            return
        if self.id_buku_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin dihapus!")
            return
        if not messagebox.askyesno(
            "Konfirmasi", "Yakin ingin menghapus data buku yang dipilih?"
        ):
            return

        if self.model.delete_buku(self.id_buku_terpilih):
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            self.id_buku_terpilih = None
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menghapus data.")

    def run(self):
        self.view.mainloop()