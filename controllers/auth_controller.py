import tkinter.messagebox as messagebox
from models.user_model import UserModel
from views.login_view import LoginView

class AuthController:
    def __init__(self, run_application=True):
        self.model = UserModel()
        self.view = LoginView()
        self.role = None
        self.run_application = run_application
        self.view.btn_login.configure(command=self.proses_login)
        self.view.protocol("WM_DELETE_WINDOW", self.tutup)

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
        self.role = role
        self.model.close()
        self.view.quit()
        self.view.destroy()
        if self.run_application:
            from controllers.buku_controller import BukuController

            BukuController(user_role=role).run()

    def tutup(self):
        self.model.close()
        self.view.quit()
        self.view.destroy()

    def run(self):
        self.view.mainloop()
        return self.role