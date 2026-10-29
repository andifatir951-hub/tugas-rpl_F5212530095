import tkinter.messagebox as messagebox
from models.user_model import UserModel
from views.login_view import LoginView
from controllers.buku_controller import BukuController

class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView()
        self.mode_admin_awal = self.model.belum_ada_pengguna()
        self.view.atur_mode_admin_awal(self.mode_admin_awal)
        self.view.btn_login.configure(command=self.proses_login)
        self.view.btn_anggota.configure(
            command=lambda: self.buka_aplikasi("anggota")
        )

    def proses_login(self):
        username = self.view.entry_username.get()
        password = self.view.entry_password.get()

        if self.mode_admin_awal:
            self.buat_admin_awal(username, password)
            return

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        user = self.model.autentikasi(username, password)

        if user:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {user['username']} ({user['role']})!")
            self.buka_aplikasi(user["role"])
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!")

    def buat_admin_awal(self, username, password):
        konfirmasi_password = self.view.entry_konfirmasi_password.get()

        if not username or not password or not konfirmasi_password:
            messagebox.showwarning("Peringatan", "Semua kolom wajib diisi!")
            return

        if password != konfirmasi_password:
            messagebox.showerror("Gagal", "Konfirmasi password tidak cocok!")
            return

        if not self.model.buat_admin_pertama(username, password):
            self.mode_admin_awal = self.model.belum_ada_pengguna()
            self.view.atur_mode_admin_awal(self.mode_admin_awal)
            messagebox.showerror(
                "Gagal", "Akun admin sudah dibuat atau username sudah digunakan."
            )
            return

        messagebox.showinfo("Berhasil", "Akun admin berhasil dibuat.")
        self.buka_aplikasi("admin")

    def buka_aplikasi(self, role):
        self.model.close()
        self.view.destroy()
        app_utama = BukuController(user_role=role)
        app_utama.run()

    def run(self):
        self.view.mainloop()