from unittest.mock import MagicMock

import main


def test_main_membuka_login_lagi_setelah_logout(monkeypatch):
    auth = MagicMock()
    auth.run.side_effect = ["admin", None]
    buku = MagicMock()
    buku.run.side_effect = [True]
    auth_controller = MagicMock(return_value=auth)
    buku_controller = MagicMock(return_value=buku)
    monkeypatch.setattr(main, "AuthController", auth_controller)
    monkeypatch.setattr(main, "BukuController", buku_controller)

    main.main()

    assert auth_controller.call_count == 2
    auth_controller.assert_called_with(run_application=False)
    buku_controller.assert_called_once_with(user_role="admin")
