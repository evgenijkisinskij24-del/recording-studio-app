from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QMessageBox)
from Data.database import DBManager


class ContractsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Справочник: Договоры")
        self.resize(700, 450)
        self.db = DBManager()
        self.init_ui()
        self.load_clients()
        self.load_contracts()

    def init_ui(self):
        layout = QVBoxLayout()

        # Выбор клиента для фильтрации/добавления (FR-03)
        self.client_selector = QComboBox()
        self.client_selector.addItem("Все клиенты", None)
        self.client_selector.currentIndexChanged.connect(self.load_contracts)
        layout.addWidget(self.client_selector)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "№ Дог.", "Начало", "Конец", "Сумма", "Статус"])
        layout.addWidget(self.table)

        # Поля ввода
        form = QHBoxLayout()
        self.num_in = QLineEdit();
        self.num_in.setPlaceholderText("№")
        self.sum_in = QLineEdit();
        self.sum_in.setPlaceholderText("Сумма")
        self.status_in = QComboBox();
        self.status_in.addItems(["Не оплачен", "Оплачен"])
        form.addWidget(self.num_in);
        form.addWidget(self.sum_in);
        form.addWidget(self.status_in)
        layout.addLayout(form)

        btns = QHBoxLayout()
        add_btn = QPushButton("Добавить договор")
        add_btn.clicked.connect(self.add_contract)
        pay_btn = QPushButton("Сменить статус оплаты (FR-07)")
        pay_btn.clicked.connect(self.toggle_payment)
        btns.addWidget(add_btn);
        btns.addWidget(pay_btn)
        layout.addLayout(btns)
        self.setLayout(layout)

    def load_clients(self):
        clients = self.db.execute_query("SELECT id, fio FROM Clients")
        for cid, fio in clients:
            self.client_selector.addItem(fio, cid)

    def load_contracts(self):
        client_id = self.client_selector.currentData()
        if client_id:
            query = "SELECT id, number, start_date, end_date, amount, status FROM Contracts WHERE client_id=?"
            res = self.db.execute_query(query, (client_id,))
        else:
            res = self.db.execute_query("SELECT id, number, start_date, end_date, amount, status FROM Contracts")

        self.table.setRowCount(0)
        for r_idx, r_data in enumerate(res):
            self.table.insertRow(r_idx)
            for c_idx, c_data in enumerate(r_data):
                self.table.setItem(r_idx, c_idx, QTableWidgetItem(str(c_data)))

    def add_contract(self):
        cid = self.client_selector.currentData()
        if not cid: return QMessageBox.warning(self, "!", "Выберите клиента")
        self.db.commit_query(
            "INSERT INTO Contracts (client_id, number, start_date, amount, status) VALUES (?, ?, '2026-05-07', ?, ?)",
            (cid, self.num_in.text(), self.sum_in.text(), self.status_in.currentText())
        )
        self.load_contracts()

    def toggle_payment(self):
        row = self.table.currentRow()
        if row < 0: return
        cid = self.table.item(row, 0).text()
        new_status = "Оплачен" if self.table.item(row, 5).text() == "Не оплачен" else "Не оплачен"
        self.db.commit_query("UPDATE Contracts SET status=? WHERE id=?", (new_status, cid))
        self.load_contracts()