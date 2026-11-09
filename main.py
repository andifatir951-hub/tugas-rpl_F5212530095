from controllers.auth_controller import AuthController
from controllers.buku_controller import BukuController


def main():
    while True:
        role = AuthController(run_application=False).run()
        if role is None:
            return

        aplikasi = BukuController(user_role=role)
        if not aplikasi.run():
            return

if __name__ == "__main__":
    main()