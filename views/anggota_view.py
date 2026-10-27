import customtkinter as ctk
from tkinter import ttk


class AnggotaView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Manajemen Anggota Perpustakaan")
        self.geometry("700x450")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        form = ctk.CTkFrame(self)
        form.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        form.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            form,
            text="Form Data Anggota",
            font=("Arial", 18, "bold"),
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

        self.entry_nama = ctk.CTkEntry(
            form,
            placeholder_text="Masukkan nama anggota",
        )
        self.entry_nama.grid(row=1, column=0, padx=15, pady=5, sticky="ew")

        self.entry_alamat = ctk.CTkEntry(
            form,
            placeholder_text="Masukkan alamat anggota",
        )
        self.entry_alamat.grid(row=2, column=0, padx=15, pady=5, sticky="ew")

        self.btn_simpan = ctk.CTkButton(
            form,
            text="Simpan Anggota",
            fg_color="green",
        )
        self.btn_simpan.grid(row=3, column=0, padx=15, pady=5, sticky="ew")

        self.btn_update = ctk.CTkButton(
            form,
            text="Perbarui Anggota",
            fg_color="blue",
        )
        self.btn_update.grid(row=4, column=0, padx=15, pady=5, sticky="ew")

        self.btn_delete = ctk.CTkButton(
            form,
            text="Hapus Anggota",
            fg_color="red",
        )
        self.btn_delete.grid(row=5, column=0, padx=15, pady=(5, 15), sticky="ew")

        daftar = ctk.CTkFrame(self)
        daftar.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        daftar.grid_columnconfigure(0, weight=1)
        daftar.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            daftar,
            text="Daftar Anggota",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.tabel = ttk.Treeview(
            daftar,
            columns=("id", "nama", "alamat"),
            show="headings",
        )
        self.tabel.heading("id", text="ID")
        self.tabel.heading("nama", text="Nama")
        self.tabel.heading("alamat", text="Alamat")
        self.tabel.column("id", width=60, anchor="center")
        self.tabel.column("nama", width=180)
        self.tabel.column("alamat", width=350)
        self.tabel.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
