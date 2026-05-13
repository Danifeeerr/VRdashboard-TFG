import requests

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from config import API_BASE
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


class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet(f"background-color: {WHITE};")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._header())
        root.addWidget(self._body(), stretch=1)
        root.addWidget(self._footer())

    def _header(self):
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet(f"background-color: {ORANGE}; border: none;")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)

        left_spacer = QWidget()
        left_spacer.setFixedWidth(120)
        left_spacer.setStyleSheet("background: transparent;")
        layout.addWidget(left_spacer)

        self.header_title = QLabel(tr("login_welcome"))
        self.header_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.header_title.setFont(font)
        self.header_title.setStyleSheet(f"color: {WHITE}; background: transparent;")
        layout.addWidget(self.header_title, stretch=1)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems([tr("lang_ca"), tr("lang_es"), tr("lang_en")])
        self.lang_combo.setCurrentIndex(LANG_CODES.index(get_lang()))
        self.lang_combo.setFixedSize(120, 34)
        self.lang_combo.setStyleSheet(_COMBO_STYLE)
        self.lang_combo.currentIndexChanged.connect(
            lambda i: self.main_window.change_language(LANG_CODES[i])
        )
        layout.addWidget(self.lang_combo)

        return header

    def _body(self):
        body = QFrame()
        body.setStyleSheet(f"background-color: {WHITE};")

        outer = QHBoxLayout(body)
        outer.setContentsMargins(0, 0, 0, 0)

        v_center = QVBoxLayout()
        v_center.setContentsMargins(0, 0, 0, 0)
        v_center.addStretch()

        form_container = QWidget()
        form_container.setFixedWidth(500)
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(20)

        self.subtitle = QLabel(tr("login_subtitle"))
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setWordWrap(True)
        font_sub = QFont()
        font_sub.setPointSize(14)
        font_sub.setBold(True)
        self.subtitle.setFont(font_sub)
        self.subtitle.setStyleSheet(f"color: {DARK_TEXT};")
        form_layout.addWidget(self.subtitle)
        form_layout.addSpacing(10)

        input_style = f"""
            QLineEdit {{
                border: 1px solid {LIGHT_BORDER};
                border-radius: 4px;
                padding: 0 12px;
                font-size: 14px;
                color: {DARK_TEXT};
                background: {WHITE};
            }}
            QLineEdit:focus {{
                border: 1px solid #A0A0A0;
            }}
        """

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(tr("username_placeholder"))
        self.username_input.setFixedHeight(42)
        self.username_input.setStyleSheet(input_style)
        form_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(tr("password_placeholder"))
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(42)
        self.password_input.setStyleSheet(input_style)
        form_layout.addWidget(self.password_input)

        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setWordWrap(True)
        font_err = QFont()
        font_err.setPointSize(10)
        self.error_label.setFont(font_err)
        self.error_label.setStyleSheet("color: #D9534F; background: transparent;")
        self.error_label.hide()
        form_layout.addWidget(self.error_label)

        self.login_btn = HoverButton(tr("login_btn"))
        self.login_btn.setFixedHeight(48)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        font_btn = QFont()
        font_btn.setPointSize(13)
        font_btn.setBold(True)
        self.login_btn.setFont(font_btn)
        self.login_btn.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_btn)

        self.note = QLabel(tr("forgot_password"))
        self.note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.note.setWordWrap(True)
        font_note = QFont()
        font_note.setPointSize(10)
        self.note.setFont(font_note)
        self.note.setStyleSheet(f"color: {DARK_TEXT}; background: transparent;")
        form_layout.addWidget(self.note)

        v_center.addWidget(form_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        v_center.addStretch()

        outer.addStretch()
        outer.addLayout(v_center)
        outer.addStretch()
        return body

    def _footer(self):
        footer = QFrame()
        footer.setFixedHeight(60)
        footer.setStyleSheet(f"background-color: {ORANGE}; border: none;")
        return footer

    def retranslate_ui(self):
        self.header_title.setText(tr("login_welcome"))
        self.subtitle.setText(tr("login_subtitle"))
        self.username_input.setPlaceholderText(tr("username_placeholder"))
        self.password_input.setPlaceholderText(tr("password_placeholder"))
        self.login_btn.setText(tr("login_btn"))
        self.note.setText(tr("forgot_password"))
        self.error_label.hide()
        self.lang_combo.blockSignals(True)
        self.lang_combo.setCurrentIndex(LANG_CODES.index(get_lang()))
        self.lang_combo.blockSignals(False)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            self._show_error(tr("err_fill_credentials"))
            return

        self.login_btn.setEnabled(False)
        self.login_btn.setText(tr("logging_in"))
        self.error_label.hide()

        try:
            response = requests.post(
                f"{API_BASE}/login",
                json={"username": username, "password": password},
                timeout=10,
            )
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                response2 = requests.get(
                    f"{API_BASE}/user",
                    params={"token": token},
                    timeout=10,
                )
                if response2.status_code == 200:
                    data2 = response2.json()
                    admin = data2.get("admin")
                    if admin == True:
                        self.main_window.go_to_main(username, token)
                        self.username_input.clear()
                        self.password_input.clear()
                    else:
                        self._show_error(tr("err_not_admin"))
            elif response.status_code == 401:
                self._show_error(tr("err_wrong_credentials"))
            else:
                self._show_error(tr("err_server_retry").format(response.status_code))
        except requests.exceptions.ConnectionError:
            self._show_error(tr("err_connection_vpn"))
        except requests.exceptions.Timeout:
            self._show_error(tr("err_timeout_retry"))
        except Exception:
            self._show_error(tr("err_unexpected_retry"))
        finally:
            self.login_btn.setEnabled(True)
            self.login_btn.setText(tr("login_btn"))

    def _show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()
