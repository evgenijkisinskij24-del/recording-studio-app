from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
from Data.database import DBManager


class ReportsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Отчеты")
        self.resize(500, 500)
        self.db = DBManager()

        layout = QVBoxLayout()
        self.result_area = QTextEdit()

        btn_debt = QPushButton("Отчет по задолженностям (FR-08)")
        btn_debt.clicked.connect(self.report_debts)

        layout.addWidget(btn_debt)
        layout.addWidget(self.result_area)
        self.setLayout(layout)

    def report_debts(self):
        query = """
            SELECT Clients.fio, Contracts.number, Contracts.amount 
            FROM Contracts 
            JOIN Clients ON Contracts.client_id = Clients.id 
            WHERE Contracts.status = 'Не оплачен'
        """
        res = self.db.execute_query(query)
        report = "ОТЧЕТ ПО ЗАДОЛЖЕННОСТЯМ:\n" + "=" * 30 + "\n"
        for fio, num, amt in res:
            report += f"Клиент: {fio} | Договор №{num} | Сумма: {amt} руб.\n"
        self.result_area.setText(report)