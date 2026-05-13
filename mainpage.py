from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from translations import tr, get_lang, LANG_CODES

ORANGE = "#F58953"
WHITE = "#FFFFFF"
YELLOW = "#FFC046"
HOVER_COLOR = "#F5A453"
DARK_TEXT = "#2C2C2A"
LIGHT_BORDER = "#CCCCCC"

_COMBO_STYLE = """
    QComboBox {
        background-color: white;
        color: #2C2C2A;
        border: none;
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 12px;
    }
    QComboBox::drop-down { border: none; }
    QComboBox QAbstractItemView {
        background: white;
        color: #2C2C2A;
        selection-background-color: #F5A453;
        selection-color: white;
    }
"""


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
        self.username_label.setText(tr("logged_user").format(username))

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

        self.logout_btn = HoverButton(tr("logout_btn"))
        self.logout_btn.setFixedSize(130, 40)
        self.logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        font_btn = QFont()
        font_btn.setPointSize(10)
        font_btn.setBold(True)
        self.logout_btn.setFont(font_btn)
        self.logout_btn.clicked.connect(self.main_window.go_to_login)
        layout.addWidget(self.logout_btn)

        self.header_title = QLabel(tr("app_title"))
        self.header_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_title = QFont()
        font_title.setPointSize(18)
        font_title.setBold(True)
        self.header_title.setFont(font_title)
        self.header_title.setStyleSheet(f"color: {WHITE}; background: transparent;")
        layout.addWidget(self.header_title, stretch=1)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems([tr("lang_ca"), tr("lang_es"), tr("lang_en")])
        self.lang_combo.setCurrentIndex(LANG_CODES.index(get_lang()))
        self.lang_combo.setFixedSize(130, 40)
        self.lang_combo.setStyleSheet(_COMBO_STYLE)
        self.lang_combo.currentIndexChanged.connect(
            lambda i: self.main_window.change_language(LANG_CODES[i])
        )
        layout.addWidget(self.lang_combo)

        return header

    def _body(self):
        body = QFrame()
        body.setStyleSheet(f"background-color: {WHITE};")

        outer = QVBoxLayout(body)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(0)

        self.username_label = QLabel("")
        font_user = QFont()
        font_user.setPointSize(10)
        self.username_label.setFont(font_user)
        self.username_label.setStyleSheet(f"color: {DARK_TEXT};")
        outer.addWidget(self.username_label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        center_layout = QVBoxLayout()
        center_layout.setSpacing(30)

        font_big = QFont()
        font_big.setPointSize(13)
        font_big.setBold(True)

        self.btn_crear = HoverButton(tr("create_user_btn"))
        self.btn_crear.setFixedSize(320, 60)
        self.btn_crear.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_crear.clicked.connect(self.main_window.go_to_new_user)
        self.btn_crear.setFont(font_big)

        self.btn_llista = HoverButton(tr("user_list_btn"))
        self.btn_llista.setFixedSize(320, 60)
        self.btn_llista.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_llista.clicked.connect(self.main_window.go_to_user_list)
        self.btn_llista.setFont(font_big)

        center_layout.addWidget(self.btn_crear, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addWidget(self.btn_llista, alignment=Qt.AlignmentFlag.AlignHCenter)

        outer.addStretch()
        outer.addLayout(center_layout)
        outer.addStretch()

        return body

    def retranslate_ui(self):
        self.header_title.setText(tr("app_title"))
        self.logout_btn.setText(tr("logout_btn"))
        if self.username:
            self.username_label.setText(tr("logged_user").format(self.username))
        self.btn_crear.setText(tr("create_user_btn"))
        self.btn_llista.setText(tr("user_list_btn"))
        self.lang_combo.blockSignals(True)
        self.lang_combo.setCurrentIndex(LANG_CODES.index(get_lang()))
        self.lang_combo.blockSignals(False)
