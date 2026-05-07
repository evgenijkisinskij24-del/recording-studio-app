import sys
from PyQt6.QtWidgets import QApplication
from Forms.auth_form import AuthForm
from Forms.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    auth = AuthForm()
    if auth.exec() == AuthForm.DialogCode.Accepted:
        window = MainWindow(auth.user_role)
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()