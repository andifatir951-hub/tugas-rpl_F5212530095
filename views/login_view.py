import customtkinter as ctk

class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login - Sistem Perpustakaan")
        self.geometry("360x430")
        self.resizable(False, False)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_judul = ctk.CTkLabel(
            self.frame, text="LOGIN SISTEM", font=("Arial", 18, "bold")
        )
        self.label_judul.pack(pady=(20, 15))

        self.entry_username = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.entry_username.pack(pady=10, padx=20, fill="x")

        # Parameter show="*" menyembunyikan karakter password
        self.entry_password = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=10, padx=20, fill="x")

        self.entry_konfirmasi_password = ctk.CTkEntry(
            self.frame, placeholder_text="Ulangi password", show="*"
        )

        self.btn_login = ctk.CTkButton(self.frame, text="Masuk", fg_color="blue")
        self.btn_login.pack(pady=20, padx=20, fill="x")

        self.btn_anggota = ctk.CTkButton(
            self.frame,
            text="Lanjutkan sebagai anggota",
            fg_color="gray",
            hover_color="gray40",
        )
        self.btn_anggota.pack(pady=(0, 15), padx=20, fill="x")

    def atur_mode_admin_awal(self, aktif):
        if aktif:
            self.title("Buat Admin - Sistem Perpustakaan")
            self.label_judul.configure(text="BUAT ADMIN PERTAMA")
            self.btn_login.configure(text="Buat Akun Admin")
            self.entry_konfirmasi_password.pack(
                after=self.entry_password, pady=10, padx=20, fill="x"
            )
        else:
            self.title("Login - Sistem Perpustakaan")
            self.label_judul.configure(text="LOGIN SISTEM")
            self.btn_login.configure(text="Masuk")
            self.entry_konfirmasi_password.pack_forget()