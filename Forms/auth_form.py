from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel
from Data.database import DBManager


class AuthForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setFixedSize(300, 150)
        self.db = DBManager()
        self.user_role = None

        layout = QVBoxLayout()

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Пароль")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_login = QPushButton("Войти")
        self.btn_login.clicked.connect(self.authenticate)

        layout.addWidget(QLabel("Введите учетные данные:"))
        layout.addWidget(self.login_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.btn_login)
        self.setLayout(layout)

    def authenticate(self):
        login = self.login_input.text()
        password = self.pass_input.text()

        user = self.db.check_user(login, password)
        if user:
            self.user_role = user[0]
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")