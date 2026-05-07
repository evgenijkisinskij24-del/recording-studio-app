from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox)
from Data.database import DBManager


class ClientsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Справочник: Клиенты")
        self.resize(600, 400)
        self.db = DBManager()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()

        # Поиск по ФИО
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по ФИО...")
        search_btn = QPushButton("Найти")
        search_btn.clicked.connect(self.search_data)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)

        # Таблица клиентов
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "ФИО", "Телефон", "Бронь", "Райдер"])
        layout.addWidget(self.table)

        # Ввод новых данных
        form_layout = QHBoxLayout()
        self.fio_input = QLineEdit()
        self.fio_input.setPlaceholderText("ФИО (обязательно)")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Телефон")
        self.booking_input = QLineEdit()
        self.booking_input.setPlaceholderText("Бронь студии")
        self.rider_input = QLineEdit()
        self.rider_input.setPlaceholderText("Райдер")

        form_layout.addWidget(self.fio_input)
        form_layout.addWidget(self.phone_input)
        form_layout.addWidget(self.booking_input)
        form_layout.addWidget(self.rider_input)
        layout.addLayout(form_layout)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add_client)
        del_btn = QPushButton("Удалить выбранного")
        del_btn.clicked.connect(self.delete_client)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_data(self, query="SELECT * FROM Clients", params=()):
        self.table.setRowCount(0)
        records = self.db.execute_query(query, params)
        for row_idx, row_data in enumerate(records):
            self.table.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def add_client(self):
        fio = self.fio_input.text()
        phone = self.phone_input.text()
        booking = self.booking_input.text()
        rider = self.rider_input.text()

        if not fio:
            QMessageBox.warning(self, "Ошибка", "Поле ФИО обязательно для заполнения!")
            return

        self.db.commit_query("INSERT INTO Clients (fio, phone, booking, rider) VALUES (?, ?, ?, ?)",
                             (fio, phone, booking, rider))
        self.load_data()
        self.fio_input.clear()  # Очистка поля после добавления

    def delete_client(self):
        row = self.table.currentRow()
        if row < 0: return
        client_id = self.table.item(row, 0).text()
        self.db.commit_query("DELETE FROM Clients WHERE id=?", (client_id,))
        self.load_data()

    def search_data(self):
        fio = self.search_input.text()
        self.load_data("SELECT * FROM Clients WHERE fio LIKE ?", ('%' + fio + '%',))