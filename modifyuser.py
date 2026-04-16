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
RED = "#D9534F"
RED_HOVER = "#C9302C"
DARK_TEXT = "#2C2C2A"
LIGHT_BORDER = "#CCCCCC"


class HoverButton(QPushButton):
    def __init__(self, text, color=YELLOW, hover_color=HOVER_COLOR):
        super().__init__(text)
        self._default = f"QPushButton {{ background-color: {color}; color: {WHITE}; border: none; border-radius: 4px; }}"
        self._hover   = f"QPushButton {{ background-color: {hover_color}; color: {WHITE}; border: none; border-radius: 4px; }}"
        self._pressed = f"QPushButton {{ background-color: {hover_color}; color: {WHITE}; border: none; border-radius: 4px; }}"
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


class ModifyUser(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.user_id = None
        self.setStyleSheet(f"background-color: {WHITE};")
        self._build_ui()

    def set_user(self, user):
        self.user_id = user["id"]
        self.title_label.setText(f"Modifica l'usuari ({user['username']})")
        self.username_input.setText(user["username"])
        if user["admin"]:
            self.radio_si.setChecked(True)
        else:
            self.radio_no.setChecked(True)
        self.password_input.clear()
        self.admin_password_input.clear()
        self.error_label.hide()

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
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        outer.addStretch()

        form_container = QWidget()
        form_container.setFixedWidth(340)
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

        font_title = QFont()
        font_title.setPointSize(11)
        font_title.setBold(True)

        font_label = QFont()
        font_label.setPointSize(9)

        # Títol amb nom d'usuari
        self.title_label = QLabel("Modifica l'usuari")
        self.title_label.setFont(font_title)
        self.title_label.setStyleSheet(f"color: {DARK_TEXT};")
        form_layout.addWidget(self.title_label)

        form_layout.addSpacing(12)

        # Nou nom d'usuari
        lbl_username = QLabel("Nou nom de l'usuari")
        lbl_username.setFont(font_label)
        lbl_username.setStyleSheet(f"color: {DARK_TEXT};")
        form_layout.addWidget(lbl_username)

        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(36)
        self.username_input.setStyleSheet(input_style)
        form_layout.addWidget(self.username_input)

        form_layout.addSpacing(10)

        # Nova contrassenya
        lbl_password = QLabel("Nova contrassenya de l'usuari")
        lbl_password.setFont(font_label)
        lbl_password.setStyleSheet(f"color: {DARK_TEXT};")
        form_layout.addWidget(lbl_password)

        self.password_input = QLineEdit()
        self.password_input.setFixedHeight(36)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(input_style)
        form_layout.addWidget(self.password_input)

        form_layout.addSpacing(10)

        # Fer administrador - radio buttons
        admin_row = QHBoxLayout()
        admin_row.setSpacing(10)
        lbl_admin = QLabel("Fer administrador a l'usuari")
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

        form_layout.addSpacing(10)

        # Contrassenya de l'administrador
        lbl_admin_pass = QLabel("Contrassenya de l'administrador")
        lbl_admin_pass.setFont(font_label)
        lbl_admin_pass.setStyleSheet(f"color: {DARK_TEXT};")
        form_layout.addWidget(lbl_admin_pass)

        self.admin_password_input = QLineEdit()
        self.admin_password_input.setFixedHeight(36)
        self.admin_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.admin_password_input.setStyleSheet(input_style)
        form_layout.addWidget(self.admin_password_input)

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

        # Botons fila 1: Modificar + Cancel·lar
        font_btn = QFont()
        font_btn.setPointSize(11)
        font_btn.setBold(True)

        btn_row1 = QHBoxLayout()
        btn_row1.setSpacing(16)

        self.modify_btn = HoverButton("Modificar usuari")
        self.modify_btn.setFixedSize(145, 48)
        self.modify_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.modify_btn.setFont(font_btn)
        self.modify_btn.clicked.connect(self.handle_modify)

        cancel_btn = HoverButton("Cancel·lar")
        cancel_btn.setFixedSize(145, 48)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setFont(font_btn)
        cancel_btn.clicked.connect(self.main_window.go_to_user_list)

        btn_row1.addWidget(self.modify_btn)
        btn_row1.addWidget(cancel_btn)
        form_layout.addLayout(btn_row1)

        form_layout.addSpacing(10)

        # Botó fila 2: El·liminar (centrat, vermell)
        btn_row2 = QHBoxLayout()
        btn_row2.setSpacing(0)

        self.delete_btn = HoverButton("El·liminar l'usuari", color=RED, hover_color=RED_HOVER)
        self.delete_btn.setFixedSize(145, 48)
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setFont(font_btn)
        self.delete_btn.clicked.connect(self.handle_delete)

        btn_row2.addWidget(self.delete_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        form_layout.addLayout(btn_row2)

        outer.addWidget(form_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        outer.addStretch()

        return body

    def handle_modify(self):
        new_username = self.username_input.text().strip()
        new_password = self.password_input.text()
        admin_password = self.admin_password_input.text()
        is_admin = self.radio_si.isChecked()

        if not new_username:
            self._show_error("El nom d'usuari no pot estar buit.")
            return

        if not admin_password:
            self._show_error("Has d'introduir la contrassenya de l'administrador.")
            return

        self.modify_btn.setEnabled(False)
        self.modify_btn.setText("Modificant...")
        self.error_label.hide()

        try:
            # Verificar identitat de l'administrador
            auth = requests.post(
                f"{API_BASE}/login",
                json={"username": self.main_window.main_page.username, "password": admin_password},
                timeout=10,
            )
            if auth.status_code == 401:
                self._show_error("Contrassenya de l'administrador incorrecta.")
                return
            if auth.status_code != 200:
                self._show_error("Error en verificar l'administrador.")
                return

            # Fer l'update
            response = requests.post(
                f"{API_BASE}/users/update",
                json={
                    "id": self.user_id,
                    "username": new_username,
                    "password_hash": new_password if new_password else None,
                    "admin": is_admin,
                },
                timeout=10,
            )
            if response.status_code == 200:
                self.main_window.go_to_user_list()
            elif response.status_code == 409:
                self._show_error("Aquest nom d'usuari ja existeix.")
            elif response.status_code == 404:
                self._show_error("Usuari no trobat.")
            else:
                self._show_error(f"Error del servidor ({response.status_code}).")
        except requests.exceptions.ConnectionError:
            self._show_error("No s'ha pogut connectar amb el servidor.")
        except requests.exceptions.Timeout:
            self._show_error("El servidor no ha respost a temps.")
        except Exception:
            self._show_error("Error inesperat. Torna-ho a intentar.")
        finally:
            self.modify_btn.setEnabled(True)
            self.modify_btn.setText("Modificar usuari")

    def handle_delete(self):
        admin_password = self.admin_password_input.text()

        if not admin_password:
            self._show_error("Has d'introduir la contrassenya de l'administrador per eliminar.")
            return

        self.delete_btn.setEnabled(False)
        self.delete_btn.setText("Eliminant...")
        self.error_label.hide()

        try:
            # Verificar identitat de l'administrador
            auth = requests.post(
                f"{API_BASE}/login",
                json={"username": self.main_window.main_page.username, "password": admin_password},
                timeout=10,
            )
            if auth.status_code == 401:
                self._show_error("Contrassenya de l'administrador incorrecta.")
                return
            if auth.status_code != 200:
                self._show_error("Error en verificar l'administrador.")
                return

            response = requests.delete(
                f"{API_BASE}/users/delete/{self.user_id}",
                params={"token": self.main_window.access_token},
                timeout=10,
            )
            if response.status_code == 200:
                self.main_window.go_to_user_list()
            elif response.status_code == 404:
                self._show_error("Usuari no trobat.")
            else:
                self._show_error(f"Error del servidor ({response.status_code}).")
        except requests.exceptions.ConnectionError:
            self._show_error("No s'ha pogut connectar amb el servidor.")
        except requests.exceptions.Timeout:
            self._show_error("El servidor no ha respost a temps.")
        except Exception:
            self._show_error("Error inesperat. Torna-ho a intentar.")
        finally:
            self.delete_btn.setEnabled(True)
            self.delete_btn.setText("El·liminar l'usuari")

    def _show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()
