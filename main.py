import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from login import LoginPage
from mainpage import MainPage
from newuser import NewUser
from userlist import UserList
from modifyuser import ModifyUser
from attempts import AttemptsPage
from assignation import AssignationPage
from translations import set_lang, tr


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr("app_title"))
        self.setMinimumSize(900, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_page = LoginPage(self)
        self.main_page = MainPage(self)
        self.new_user = NewUser(self)
        self.user_list = UserList(self)
        self.modify_user = ModifyUser(self)
        self.attempts_page = AttemptsPage(self)
        self.assignation_page = AssignationPage(self)

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.main_page)
        self.stack.addWidget(self.new_user)
        self.stack.addWidget(self.user_list)
        self.stack.addWidget(self.modify_user)
        self.stack.addWidget(self.attempts_page)
        self.stack.addWidget(self.assignation_page)

        self.access_token = None
        self.stack.setCurrentWidget(self.login_page)

    def change_language(self, lang):
        set_lang(lang)
        self.setWindowTitle(tr("app_title"))
        for page in [
            self.login_page, self.main_page, self.new_user,
            self.user_list, self.modify_user, self.attempts_page,
            self.assignation_page,
        ]:
            page.retranslate_ui()

    def go_to_main(self, username, token):
        self.access_token = token
        self.main_page.set_username(username)
        self.stack.setCurrentWidget(self.main_page)

    def go_to_login(self):
        self.stack.setCurrentWidget(self.login_page)

    def go_to_new_user(self):
        self.new_user.set_username(self.main_page.username)
        self.stack.setCurrentWidget(self.new_user)

    def go_to_main_page(self):
        self.stack.setCurrentWidget(self.main_page)

    def go_to_user_list(self):
        self.stack.setCurrentWidget(self.user_list)

    def go_to_modify_user(self, user):
        self.modify_user.set_user(user)
        self.stack.setCurrentWidget(self.modify_user)

    def go_to_attempts(self, user):
        self.attempts_page.set_user(user)
        self.stack.setCurrentWidget(self.attempts_page)

    def go_to_assignation(self, user):
        self.assignation_page.set_user(user)
        self.stack.setCurrentWidget(self.assignation_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
