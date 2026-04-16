import requests

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QCheckBox, QScrollArea
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
ROW_BG = "#FAE5D3"


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


class UserList(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet(f"background-color: {WHITE};")
        self._build_ui()

    def set_username(self, username):
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

        btn_back = HoverButton("Pàgina principal")
        btn_back.setFixedSize(150, 40)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        font_btn = QFont()
        font_btn.setPointSize(10)
        font_btn.setBold(True)
        btn_back.setFont(font_btn)
        btn_back.clicked.connect(self.main_window.go_to_main_page)
        layout.addWidget(btn_back)

        return header

    def _body(self):
        body = QFrame()
        body.setStyleSheet(f"background-color: {WHITE};")

        outer = QVBoxLayout(body)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(12)

        # Títol filtre
        lbl_filtre = QLabel("Filtre d'usuaris")
        font_filtre = QFont()
        font_filtre.setPointSize(10)
        font_filtre.setBold(True)
        lbl_filtre.setFont(font_filtre)
        lbl_filtre.setStyleSheet(f"color: {DARK_TEXT};")
        outer.addWidget(lbl_filtre, alignment=Qt.AlignmentFlag.AlignLeft)

        # Filtre box
        filter_frame = QFrame()
        filter_frame.setStyleSheet(f"border: 1px solid {LIGHT_BORDER}; border-radius: 4px; background: {WHITE};")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(12, 8, 12, 8)
        filter_layout.setSpacing(12)

        lbl_nom = QLabel("Nom d'usuari")
        lbl_nom.setStyleSheet(f"color: {DARK_TEXT}; border: none;")
        font_lbl = QFont()
        font_lbl.setPointSize(9)
        lbl_nom.setFont(font_lbl)

        self.filter_input = QLineEdit()
        self.filter_input.setFixedSize(200, 30)
        self.filter_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {LIGHT_BORDER};
                border-radius: 4px;
                padding: 0 8px;
                font-size: 12px;
                color: {DARK_TEXT};
                background: {WHITE};
            }}
        """)

        lbl_admin = QLabel("Administrador:")
        lbl_admin.setStyleSheet(f"color: {DARK_TEXT}; border: none;")
        lbl_admin.setFont(font_lbl)

        self.filter_admin_check = QCheckBox()
        self.filter_admin_check.setStyleSheet("border: none;")

        btn_cerca = HoverButton("Cerca")
        btn_cerca.setFixedSize(90, 34)
        btn_cerca.setCursor(Qt.CursorShape.PointingHandCursor)
        font_btn = QFont()
        font_btn.setPointSize(10)
        font_btn.setBold(True)
        btn_cerca.setFont(font_btn)
        btn_cerca.clicked.connect(self.load_users)

        filter_layout.addWidget(lbl_nom)
        filter_layout.addWidget(self.filter_input)
        filter_layout.addWidget(lbl_admin)
        filter_layout.addWidget(self.filter_admin_check)
        filter_layout.addWidget(btn_cerca)
        filter_layout.addStretch()

        outer.addWidget(filter_frame)

        # Àrea de scroll per les files d'usuaris
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        self.list_container = QWidget()
        self.list_container.setStyleSheet(f"background: {WHITE};")
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10)
        self.list_layout.addStretch()

        scroll.setWidget(self.list_container)
        outer.addWidget(scroll, stretch=1)

        return body

    def showEvent(self, event):
        super().showEvent(event)
        self.load_users()

    def load_users(self):
        username_filter = self.filter_input.text().strip().lower()
        admin_filter = self.filter_admin_check.isChecked()

        try:
            response = requests.get(
                f"{API_BASE}/users",
                params={"token": self.main_window.access_token},
                timeout=10,
            )
            if response.status_code != 200:
                return
            users = response.json()
        except Exception:
            return

        # Aplicar filtres
        if username_filter:
            users = [u for u in users if username_filter in u["username"].lower()]
        if admin_filter:
            users = [u for u in users if u["admin"]]

        # Netejar llista
        while self.list_layout.count() > 1:
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Afegir files
        for user in users:
            assignations = self._get_assignation_count(user["id"])
            row = self._build_user_row(user, assignations)
            self.list_layout.insertWidget(self.list_layout.count() - 1, row)

    def _get_assignation_count(self, user_id):
        try:
            response = requests.get(
                f"{API_BASE}/assignation/{user_id}",
                params={"token": self.main_window.access_token},
                timeout=10,
            )
            if response.status_code == 200:
                return len(response.json())
        except Exception:
            pass
        return 0

    def _build_user_row(self, user, assignation_count):
        row = QFrame()
        row.setStyleSheet(f"""
            QFrame {{
                background-color: {ROW_BG};
                border-radius: 6px;
                border: none;
            }}
        """)
        row.setFixedHeight(60)

        layout = QHBoxLayout(row)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(20)

        font_row = QFont()
        font_row.setPointSize(9)
        font_row.setBold(True)

        admin_text = "Sí" if user["admin"] else "No"

        lbl_username = QLabel(user["username"])
        lbl_username.setFont(font_row)
        lbl_username.setStyleSheet(f"color: {DARK_TEXT};")
        lbl_username.setFixedWidth(150)

        lbl_admin = QLabel(f"Administrador: {admin_text}")
        lbl_admin.setFont(font_row)
        lbl_admin.setStyleSheet(f"color: {DARK_TEXT};")
        lbl_admin.setFixedWidth(160)

        lbl_assignacions = QLabel(f"Entrenaments assignats: {assignation_count}")
        lbl_assignacions.setFont(font_row)
        lbl_assignacions.setStyleSheet(f"color: {DARK_TEXT};")

        font_btn = QFont()
        font_btn.setPointSize(10)
        font_btn.setBold(True)

        btn_intents = HoverButton("Intents")
        btn_intents.setFixedSize(90, 36)
        btn_intents.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_intents.setFont(font_btn)
        btn_intents.clicked.connect(lambda _, u=user: self.main_window.go_to_attempts(u))

        btn_assignar = HoverButton("Assignar entrenament")
        btn_assignar.setFixedSize(180, 36)
        btn_assignar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_assignar.setFont(font_btn)
        btn_assignar.clicked.connect(lambda _, u=user: self.main_window.go_to_assignation(u))

        btn_modificar = HoverButton("Modificar")
        btn_modificar.setFixedSize(100, 36)
        btn_modificar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_modificar.setFont(font_btn)
        btn_modificar.clicked.connect(lambda _, u=user: self.main_window.go_to_modify_user(u))

        layout.addWidget(lbl_username)
        layout.addWidget(lbl_admin)
        layout.addWidget(lbl_assignacions)
        layout.addStretch()
        layout.addWidget(btn_intents)
        layout.addWidget(btn_assignar)
        layout.addWidget(btn_modificar)

        return row
