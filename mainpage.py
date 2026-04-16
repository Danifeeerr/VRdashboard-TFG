from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


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


class MainPage(QWidget):
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

        # Botó tancar sessió (esquerra)
        logout_btn = HoverButton("Tancar sessió")
        logout_btn.setFixedSize(130, 40)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        font_btn = QFont()
        font_btn.setPointSize(10)
        font_btn.setBold(True)
        logout_btn.setFont(font_btn)
        logout_btn.clicked.connect(self.main_window.go_to_login)
        layout.addWidget(logout_btn)

        # Títol centrat
        title = QLabel("Programa de monitorament")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_title = QFont()
        font_title.setPointSize(18)
        font_title.setBold(True)
        title.setFont(font_title)
        title.setStyleSheet(f"color: {WHITE}; background: transparent;")
        layout.addWidget(title, stretch=1)

        # Espai dret per equilibrar el botó
        spacer = QWidget()
        spacer.setFixedWidth(130)
        spacer.setStyleSheet("background: transparent;")
        layout.addWidget(spacer)

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

        # Botons centrats
        center_layout = QVBoxLayout()
        center_layout.setSpacing(30)

        btn_crear = HoverButton("Crear usuari")
        btn_crear.setFixedSize(320, 60)
        btn_crear.setCursor(Qt.CursorShape.PointingHandCursor)
        
        font_big = QFont()
        font_big.setPointSize(13)
        font_big.setBold(True)

        btn_crear.clicked.connect(self.main_window.go_to_new_user)
        btn_crear.setFont(font_big)

        btn_llista = HoverButton("Llista d'usuaris")
        btn_llista.setFixedSize(320, 60)
        btn_llista.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_llista.clicked.connect(self.main_window.go_to_user_list)
        btn_llista.setFont(font_big)

        center_layout.addWidget(btn_crear, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addWidget(btn_llista, alignment=Qt.AlignmentFlag.AlignHCenter)

        outer.addStretch()
        outer.addLayout(center_layout)
        outer.addStretch()

        return body