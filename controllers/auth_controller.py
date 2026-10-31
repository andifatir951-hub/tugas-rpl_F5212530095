import tkinter.messagebox as messagebox
from models.user_model import UserModel
from views.login_view import LoginView
from controllers.buku_controller import BukuController

class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView()
        self.view.btn_login.configure(command=self.proses_login)

    def proses_login(self):
        username = self.view.entry_username.get()
        password = self.view.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        user = self.model.autentikasi(username, password)

        if user:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {user['username']} ({user['role']})!")
            self.buka_aplikasi(user["role"])
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!")

    def buka_aplikasi(self, role):
        self.model.close()
        self.view.destroy()
        app_utama = BukuController(user_role=role)
        app_utama.run()

    def run(self):
        self.view.mainloop()