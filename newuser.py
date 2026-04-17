import requests

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from config import API_BASE

ORANGE = "#F58953"
WHITE = "#FFFFFF"
YELLOW = "#FFC046"
HOVER_COLOR = "#F5A453"
DARK_TEXT = "#2C2C2A"
LIGHT_BORDER = "#CCCCCC"


class HoverButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self._default = f"QPushButton {{ background-color: {YELLOW}; color: {WHITE}; border: none; border-radius: 4px; }}"
        self._hover   = f"QPushButton {{ background-color: {HOVER_COLOR}; color: {WHITE}; border: none; border-radius: 4px; }}"
        self._pressed = f"QPushButton {{ background-color: {HOVER_COLOR}; color: {WHITE}; border: none; border-radius: 4px; }}"
        self.setStyleSheet(self._default)

    def enterEvent(self, event):
        self.setStyleSheet(self._hover)

    def leaveEvent(self, event):
        self.setStyleSheet(self._default)

    def mousePressEvent(self, event):
        self.setStyleSheet(self._pressed)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setStyleSheet(self._hover)
        super().mouseReleaseEvent(event)


class NewUser(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.username = ""
        self.setStyleSheet(f"background-color: {WHITE};")
        self._build_ui()

    def set_username(self, username):
        self.username = username
        self.username_label.setText(f"Nom de l'usuari: {username}")

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._header())
        root.addWidget(self._body(), stretch=1)

    def _header(self):
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet(f"background-color: {ORANGE}; border: none;")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 0, 16, 0)

        title = QLabel("Programa de monitorament")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_title = QFont()
        font_title.setPointSize(18)
        font_title.setBold(True)
        title.setFont(font_title)
        title.setStyleSheet(f"color: {WHITE}; background: transparent;")
        layout.addWidget(title, stretch=1)

        return header

    def _body(self):
        body = QFrame()
        body.setStyleSheet(f"background-color: {WHITE};")

        outer = QVBoxLayout(body)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(0)

        # Nom de l'usuari (dalt a l'esquerra)
        self.username_label = QLabel("Nom de l'usuari")
        font_user = QFont()
        font_user.setPointSize(10)
        self.username_label.setFont(font_user)
        self.username_label.setStyleSheet(f"color: {DARK_TEXT};")
        outer.addWidget(self.username_label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Formulari centrat
        outer.addStretch()

        form_container = QWidget()
        form_container.setFixedWidth(320)
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(6)

        input_style = f"""
            QLineEdit {{
                border: 1px solid {LIGHT_BORDER};
                border-radius: 4px;
                padding: 0 10px;
                font-size: 13px;
                color: {DARK_TEXT};
                background: {WHITE};
            }}
            QLineEdit:focus {{
                border: 1px solid #A0A0A0;
            }}
        """

        font_label = QFont()
        font_label.setPointSize(9)

        # Nom del nou usuari
        lbl_username = QLabel("Nom del nou usuari")
        lbl_username.setFont(font_label)
        lbl_username.setStyleSheet(f"color: {DARK_TEXT};")
        form_layout.addWidget(lbl_username)

        self.new_username_input = QLineEdit()
        self.new_username_input.setFixedHeight(36)
        self.new_username_input.setStyleSheet(input_style)
        form_layout.addWidget(self.new_username_input)

        form_layout.addSpacing(10)

        # Contrasenya
        lbl_password = QLabel("Contrasenya")
        lbl_password.setFont(font_label)
        lbl_password.setStyleSheet(f"color: {DARK_TEXT};")
        form_layout.addWidget(lbl_password)

        self.password_input = QLineEdit()
        self.password_input.setFixedHeight(36)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(input_style)
        form_layout.addWidget(self.password_input)

        form_layout.addSpacing(10)

        # Repeteix la contrasenya
        lbl_repeat = QLabel("Repeteix la contrasenya")
        lbl_repeat.setFont(font_label)
        lbl_repeat.setStyleSheet(f"color: {DARK_TEXT};")
        form_layout.addWidget(lbl_repeat)

        self.repeat_input = QLineEdit()
        self.repeat_input.setFixedHeight(36)
        self.repeat_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.repeat_input.setStyleSheet(input_style)
        form_layout.addWidget(self.repeat_input)

        form_layout.addSpacing(14)

        # Usuari administrador (label + radio buttons)
        admin_row = QHBoxLayout()
        admin_row.setSpacing(10)
        lbl_admin = QLabel("Usuari administrador")
        lbl_admin.setFont(font_label)
        lbl_admin.setStyleSheet(f"color: {DARK_TEXT};")
        self.radio_si = QRadioButton("Sí")
        self.radio_si.setStyleSheet(f"color: {DARK_TEXT}; background: transparent;")
        self.radio_no = QRadioButton("No")
        self.radio_no.setStyleSheet(f"color: {DARK_TEXT}; background: transparent;")
        self.radio_no.setChecked(True)
        self.admin_group = QButtonGroup(self)
        self.admin_group.addButton(self.radio_si)
        self.admin_group.addButton(self.radio_no)
        admin_row.addWidget(lbl_admin)
        admin_row.addWidget(self.radio_si)
        admin_row.addWidget(self.radio_no)
        admin_row.addStretch()
        form_layout.addLayout(admin_row)

        form_layout.addSpacing(20)

        # Missatge d'error
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setWordWrap(True)
        font_err = QFont()
        font_err.setPointSize(9)
        self.error_label.setFont(font_err)
        self.error_label.setStyleSheet("color: #D9534F; background: transparent;")
        self.error_label.hide()
        form_layout.addWidget(self.error_label)

        # Botons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(16)

        font_btn = QFont()
        font_btn.setPointSize(11)
        font_btn.setBold(True)

        self.create_btn = HoverButton("Crear usuari")
        self.create_btn.setFixedSize(145, 48)
        self.create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.create_btn.setFont(font_btn)
        self.create_btn.clicked.connect(self.handle_create)

        cancel_btn = HoverButton("Cancel·lar")
        cancel_btn.setFixedSize(145, 48)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setFont(font_btn)
        cancel_btn.clicked.connect(self.main_window.go_to_main_page)

        btn_row.addWidget(self.create_btn)
        btn_row.addWidget(cancel_btn)
        form_layout.addLayout(btn_row)

        outer.addWidget(form_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        outer.addStretch()

        return body

    def handle_create(self):
        username = self.new_username_input.text().strip()
        password = self.password_input.text()
        repeat = self.repeat_input.text()
        is_admin = self.radio_si.isChecked()

        if not username or not password or not repeat:
            self._show_error("Si us plau, omple tots els camps.")
            return

        if password != repeat:
            self._show_error("Les contrasenyes no coincideixen.")
            return

        self.create_btn.setEnabled(False)
        self.create_btn.setText("Creant...")
        self.error_label.hide()

        try:
            response = requests.post(
                f"{API_BASE}/users/new",
                json={"username": username, "password_hash": password, "admin": is_admin},
                timeout=10,
            )
            if response.status_code == 200:
                self.new_username_input.clear()
                self.password_input.clear()
                self.repeat_input.clear()
                self.radio_no.setChecked(True)
                self.main_window.go_to_main_page()
            elif response.status_code == 409:
                self._show_error("El nom d'usuari ja existeix")
            else:
                self._show_error(f"Error del servidor ({response.status_code}). Torna-ho a intentar.")
        except requests.exceptions.ConnectionError:
            self._show_error("No s'ha pogut connectar amb el servidor.")
        except requests.exceptions.Timeout:
            self._show_error("El servidor no ha respost a temps.")
        except Exception:
            self._show_error("Error inesperat. Torna-ho a intentar.")
        finally:
            self.create_btn.setEnabled(True)
            self.create_btn.setText("Crear usuari")

    def _show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()
