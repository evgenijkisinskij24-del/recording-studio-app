from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QComboBox, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QLabel)
from Data.database import DBManager
import datetime


class RequestsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация и просмотр обращений")
        self.resize(900, 500)
        self.db = DBManager()
        self.init_ui()
        self.load_clients()
        self.load_requests()  # Загрузка списка при открытии

    def init_ui(self):
        layout = QVBoxLayout()

        # Блок фильтрации и выбора
        layout.addWidget(QLabel("Выберите клиента и договор:"))
        self.client_cb = QComboBox()
        self.contract_cb = QComboBox()
        self.client_cb.currentIndexChanged.connect(self.update_contracts)
        layout.addWidget(self.client_cb)
        layout.addWidget(self.contract_cb)

        # Поля ввода по ТЗ (FR-04)
        self.title_in = QLineEdit();
        self.title_in.setPlaceholderText("Название (FR-04)")
        self.artist_in = QLineEdit();
        self.artist_in.setPlaceholderText("Исполнитель")
        self.type_cb = QComboBox();
        self.type_cb.addItems(["SP", "LP", "Ep"])
        self.percent_in = QLineEdit();
        self.percent_in.setPlaceholderText("% отчислений")

        for w in [self.title_in, self.artist_in, self.type_cb, self.percent_in]:
            layout.addWidget(w)

        btn_save = QPushButton("Сохранить заявку")
        btn_save.clicked.connect(self.save_request)
        layout.addWidget(btn_save)


        layout.addWidget(QLabel("Список всех зарегистрированных обращений:"))
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Договор ID", "Название", "Тип", "Статус", "Дата","Исполнитель"])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_clients(self):
        res = self.db.execute_query("SELECT id, fio FROM Clients")
        for cid, fio in res: self.client_cb.addItem(fio, cid)

    def update_contracts(self):
        self.contract_cb.clear()
        cid = self.client_cb.currentData()
        res = self.db.execute_query("SELECT id, number FROM Contracts WHERE client_id=?", (cid,))
        for coid, num in res: self.contract_cb.addItem(f"Договор №{num}", coid)

    def load_requests(self):
        """Метод для отображения документов в заявках"""
        query = "SELECT id, contract_id, title, album_type, status, request_date, artist FROM Requests"
        res = self.db.execute_query(query)
        self.table.setRowCount(0)
        for r_idx, r_data in enumerate(res):
            self.table.insertRow(r_idx)
            for c_idx, c_data in enumerate(r_data):
                self.table.setItem(r_idx, c_idx, QTableWidgetItem(str(c_data)))

    def save_request(self):
        coid = self.contract_cb.currentData()
        if not coid: return
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        query = """INSERT INTO Requests (contract_id, request_date, album_type, status, title, artist, percent, created_at) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        self.db.commit_query(query, (coid, now, self.type_cb.currentText(), "Направлен",
                                     self.title_in.text(), self.artist_in.text(), self.percent_in.text(), now))
        self.load_requests()  # Обновляем таблицу после сохранения