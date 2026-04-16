import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from login import LoginPage
from mainpage import MainPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Programa de monitorament")
        self.setMinimumSize(900, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Crear les pàgines passant-li self (MainWindow)
        self.login_page = LoginPage(self)
        self.main_page = MainPage(self)

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.main_page)

        self.access_token = None

        # Obre la pagina de login a l'iniciar
        self.stack.setCurrentWidget(self.login_page)


    def go_to_main(self, username, token):
        self.access_token = token
        self.main_page.set_username(username)
        self.stack.setCurrentWidget(self.main_page)

    def go_to_login(self):
        self.stack.setCurrentWidget(self.login_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())