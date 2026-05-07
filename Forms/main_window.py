from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QAction
from Forms.clients_form import ClientsForm
from Forms.contracts_form import ContractsForm
from Forms.requests_form import RequestsForm
from Forms.reports_form import ReportsForm

class MainWindow(QMainWindow):
    def __init__(self, role):
        super().__init__()
        self.setWindowTitle("Студия звукозаписи")
        self.resize(800, 600)
        self.role = role

        menu_bar = self.menuBar()
        dict_menu = menu_bar.addMenu("Справочники")

        # Подключаем справочник Клиентов
        action_clients = QAction("Клиенты", self)
        action_clients.triggered.connect(self.open_clients)
        dict_menu.addAction(action_clients)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Добро пожаловать. Роль: {self.role}"))
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        #dict_menu = menu_bar.addMenu("Справочники")
        #dict_menu.addAction("Клиенты").triggered.connect(lambda: self.show_f(ClientsForm))
        dict_menu.addAction("Договоры").triggered.connect(lambda: self.show_f(ContractsForm))

        doc_menu = menu_bar.addMenu("Документы")
        doc_menu.addAction("Новая заявка").triggered.connect(lambda: self.show_f(RequestsForm))

        rep_menu = menu_bar.addMenu("Отчеты")
        rep_menu.addAction("Задолженности").triggered.connect(lambda: self.show_f(ReportsForm))

    def open_clients(self):
        self.clients_form = ClientsForm()
        self.clients_form.show()



    def show_f(self, form_class):
        self.current_f = form_class()
        self.current_f.show()