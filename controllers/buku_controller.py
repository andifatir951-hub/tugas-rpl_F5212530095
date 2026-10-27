import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self):
        # Inisialisasi Model dan View
        self.model = BukuModel()
        self.view = BukuView()
        self.id_buku_terpilih = None
        
        # Binding (mengikat) tombol di View dengan fungsi di Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.perbarui_data)
        self.view.btn_delete.configure(command=self.hapus_data)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_data)
        
        # Memuat data ke tabel saat aplikasi pertama kali dibuka
        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Mengosongkan isi tabel di View terlebih dahulu
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
            
        # Mengambil data dari Model (database)
        data_buku = self.model.get_all_buku()
        
        # Memasukkan data baru ke dalam tabel View
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    def pilih_data(self, _event=None):
        pilihan = self.view.tabel.selection()
        if not pilihan:
            self.id_buku_terpilih = None
            return

        nilai = self.view.tabel.item(pilihan[0], "values")
        self.id_buku_terpilih = nilai[0]
        self.view.entry_judul.delete(0, "end")
        self.view.entry_judul.insert(0, nilai[1])
        self.view.entry_penulis.delete(0, "end")
        self.view.entry_penulis.insert(0, nilai[2])
        self.view.entry_tahun.delete(0, "end")
        self.view.entry_tahun.insert(0, nilai[3])

    def bersihkan_form(self):
        self.view.entry_judul.delete(0, "end")
        self.view.entry_penulis.delete(0, "end")
        self.view.entry_tahun.delete(0, "end")
        self.id_buku_terpilih = None
        pilihan = self.view.tabel.selection()
        if pilihan:
            self.view.tabel.selection_remove(*pilihan)
            
    def simpan_data(self):
        # Mengambil teks dari kotak input di View
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()
        
        # Validasi Form Kosong
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
            
        # Mengirim data ke Model untuk disimpan
        berhasil = self.model.create_buku(judul, penulis, tahun)
        
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            # Bersihkan form input
            self.bersihkan_form()
            # Muat ulang tabel agar data terbaru muncul
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def perbarui_data(self):
        if self.id_buku_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin diperbarui!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_buku(
            self.id_buku_terpilih, judul, penulis, tahun
        )
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def hapus_data(self):
        if self.id_buku_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin dihapus!")
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi", "Yakin ingin menghapus data buku yang dipilih?"
        )
        if not konfirmasi:
            return

        berhasil = self.model.delete_buku(self.id_buku_terpilih)
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")
            
    # Fungsi untuk menyalakan aplikasi
    def run(self):
        self.view.mainloop()