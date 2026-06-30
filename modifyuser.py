import requests

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from config import API_BASE
from translations import tr

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
        self._current_username = None
        self.setStyleSheet(f"background-color: {WHITE};")
        self._build_ui()

    def set_user(self, user):
        self.user_id = user["id"]
        self._current_username = user["username"]
        self.title_label.setText(tr("modify_user_title_named").format(user["username"]))
        self.username_input.setText(user["username"])
        if user["admin"]:
            self.radio_si.setChecked(True)
        else:
            self.radio_no.setChecked(True)
        self.password_input.clear()
        self.admin_password_input.clear()
        self.error_label.hide()
        self.confirm_frame.hide()
        self.modify_btn.show()
        self.cancel_btn.show()
        self.delete_btn.show()

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

        self.header_title = QLabel(tr("app_title"))
        self.header_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_title = QFont()
        font_title.setPointSize(18)
        font_title.setBold(True)
        self.header_title.setFont(font_title)
        self.header_title.setStyleSheet(f"color: {WHITE}; background: transparent;")
        layout.addWidget(self.header_title, stretch=1)

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

        self.title_label = QLabel(tr("modify_user_title"))
        self.title_label.setFont(font_title)
        self.title_label.setStyleSheet(f"color: {DARK_TEXT};")
        form_layout.addWidget(self.title_label)

        form_layout.addSpacing(12)

        self.lbl_new_username = QLabel(tr("new_username_field"))
        self.lbl_new_username.setFont(font_label)
        self.lbl_new_username.setStyleSheet(f"color: {DARK_TEXT};")
        form_layout.addWidget(self.lbl_new_username)

        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(36)
        self.username_input.setStyleSheet(input_style)
        form_layout.addWidget(self.username_input)

        form_layout.addSpacing(10)

        self.lbl_password = QLabel(tr("new_password_field"))
        self.lbl_password.setFont(font_label)
        self.lbl_password.setStyleSheet(f"color: {DARK_TEXT};")
        form_layout.addWidget(self.lbl_password)

        self.password_input = QLineEdit()
        self.password_input.setFixedHeight(36)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(input_style)
        form_layout.addWidget(self.password_input)

        form_layout.addSpacing(10)

        admin_row = QHBoxLayout()
        admin_row.setSpacing(10)
        self.lbl_make_admin = QLabel(tr("make_admin_label"))
        self.lbl_make_admin.setFont(font_label)
        self.lbl_make_admin.setStyleSheet(f"color: {DARK_TEXT};")

        self.radio_si = QRadioButton(tr("yes"))
        self.radio_si.setStyleSheet(f"color: {DARK_TEXT}; background: transparent;")
        self.radio_no = QRadioButton(tr("no"))
        self.radio_no.setStyleSheet(f"color: {DARK_TEXT}; background: transparent;")
        self.radio_no.setChecked(True)

        self.admin_group = QButtonGroup(self)
        self.admin_group.addButton(self.radio_si)
        self.admin_group.addButton(self.radio_no)

        admin_row.addWidget(self.lbl_make_admin)
        admin_row.addWidget(self.radio_si)
        admin_row.addWidget(self.radio_no)
        admin_row.addStretch()
        form_layout.addLayout(admin_row)

        form_layout.addSpacing(10)

        self.lbl_admin_pass = QLabel(tr("admin_password_label"))
        self.lbl_admin_pass.setFont(font_label)
        self.lbl_admin_pass.setStyleSheet(f"color: {DARK_TEXT};")
        form_layout.addWidget(self.lbl_admin_pass)

        self.admin_password_input = QLineEdit()
        self.admin_password_input.setFixedHeight(36)
        self.admin_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.admin_password_input.setStyleSheet(input_style)
        form_layout.addWidget(self.admin_password_input)

        form_layout.addSpacing(20)

        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setWordWrap(True)
        font_err = QFont()
        font_err.setPointSize(9)
        self.error_label.setFont(font_err)
        self.error_label.setStyleSheet("color: #D9534F; background: transparent;")
        self.error_label.hide()
        form_layout.addWidget(self.error_label)

        font_btn = QFont()
        font_btn.setPointSize(11)
        font_btn.setBold(True)

        btn_row1 = QHBoxLayout()
        btn_row1.setSpacing(16)

        self.modify_btn = HoverButton(tr("modify_user_btn"))
        self.modify_btn.setFixedSize(145, 48)
        self.modify_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.modify_btn.setFont(font_btn)
        self.modify_btn.clicked.connect(self.handle_modify)

        self.cancel_btn = HoverButton(tr("cancel_btn"))
        self.cancel_btn.setFixedSize(145, 48)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setFont(font_btn)
        self.cancel_btn.clicked.connect(self.main_window.go_to_user_list)

        btn_row1.addWidget(self.modify_btn)
        btn_row1.addWidget(self.cancel_btn)
        form_layout.addLayout(btn_row1)

        form_layout.addSpacing(10)

        btn_row2 = QHBoxLayout()
        btn_row2.setSpacing(0)

        self.delete_btn = HoverButton(tr("delete_user_btn"), color=RED, hover_color=RED_HOVER)
        self.delete_btn.setFixedSize(145, 48)
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setFont(font_btn)
        self.delete_btn.clicked.connect(self.handle_delete)

        btn_row2.addWidget(self.delete_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        form_layout.addLayout(btn_row2)

        form_layout.addSpacing(10)

        self.confirm_frame = QFrame()
        self.confirm_frame.setStyleSheet("background: transparent;")
        confirm_layout = QVBoxLayout(self.confirm_frame)
        confirm_layout.setContentsMargins(0, 0, 0, 0)
        confirm_layout.setSpacing(12)

        self.confirm_label = QLabel("")
        self.confirm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.confirm_label.setWordWrap(True)
        self.confirm_label.setFont(font_btn)
        self.confirm_label.setStyleSheet(f"color: {DARK_TEXT}; background: transparent;")
        confirm_layout.addWidget(self.confirm_label)

        confirm_btn_row = QHBoxLayout()
        confirm_btn_row.setSpacing(16)

        self.confirm_yes_btn = HoverButton(tr("confirm_delete_yes_btn"), color=RED, hover_color=RED_HOVER)
        self.confirm_yes_btn.setFixedSize(145, 48)
        self.confirm_yes_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.confirm_yes_btn.setFont(font_btn)
        self.confirm_yes_btn.clicked.connect(self._do_delete)

        self.confirm_no_btn = HoverButton(tr("confirm_delete_no_btn"))
        self.confirm_no_btn.setFixedSize(145, 48)
        self.confirm_no_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.confirm_no_btn.setFont(font_btn)
        self.confirm_no_btn.clicked.connect(self._cancel_confirm)

        confirm_btn_row.addWidget(self.confirm_yes_btn)
        confirm_btn_row.addWidget(self.confirm_no_btn)
        confirm_layout.addLayout(confirm_btn_row)

        self.confirm_frame.hide()
        form_layout.addWidget(self.confirm_frame)

        outer.addWidget(form_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        outer.addStretch()

        return body

    def retranslate_ui(self):
        self.header_title.setText(tr("app_title"))
        if self._current_username:
            self.title_label.setText(tr("modify_user_title_named").format(self._current_username))
        else:
            self.title_label.setText(tr("modify_user_title"))
        self.lbl_new_username.setText(tr("new_username_field"))
        self.lbl_password.setText(tr("new_password_field"))
        self.lbl_make_admin.setText(tr("make_admin_label"))
        self.radio_si.setText(tr("yes"))
        self.radio_no.setText(tr("no"))
        self.lbl_admin_pass.setText(tr("admin_password_label"))
        self.modify_btn.setText(tr("modify_user_btn"))
        self.cancel_btn.setText(tr("cancel_btn"))
        self.delete_btn.setText(tr("delete_user_btn"))
        self.confirm_yes_btn.setText(tr("confirm_delete_yes_btn"))
        self.confirm_no_btn.setText(tr("confirm_delete_no_btn"))
        if self.confirm_frame.isVisible() and self._current_username:
            self.confirm_label.setText(tr("confirm_delete_msg").format(self._current_username))
        self.error_label.hide()

    def handle_modify(self):
        new_username = self.username_input.text().strip()
        new_password = self.password_input.text()
        admin_password = self.admin_password_input.text()
        is_admin = self.radio_si.isChecked()

        if not new_username:
            self._show_error(tr("err_empty_username"))
            return

        if not admin_password:
            self._show_error(tr("err_need_admin_pass"))
            return

        self.modify_btn.setEnabled(False)
        self.modify_btn.setText(tr("modifying"))
        self.error_label.hide()

        try:
            auth = requests.post(
                f"{API_BASE}/login",
                json={"username": self.main_window.main_page.username, "password": admin_password},
                timeout=10,
            )
            if auth.status_code == 401:
                self._show_error(tr("err_wrong_admin_pass"))
                return
            if auth.status_code != 200:
                self._show_error(tr("err_verify_admin"))
                return

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
                self._show_error(tr("err_username_taken"))
            elif response.status_code == 404:
                self._show_error(tr("err_user_not_found"))
            else:
                self._show_error(tr("err_server").format(response.status_code))
        except requests.exceptions.ConnectionError:
            self._show_error(tr("err_connection"))
        except requests.exceptions.Timeout:
            self._show_error(tr("err_timeout"))
        except Exception:
            self._show_error(tr("err_unexpected_retry"))
        finally:
            self.modify_btn.setEnabled(True)
            self.modify_btn.setText(tr("modify_user_btn"))

    def handle_delete(self):
        admin_password = self.admin_password_input.text()

        if not admin_password:
            self._show_error(tr("err_need_admin_pass_delete"))
            return

        self.delete_btn.setEnabled(False)
        self.delete_btn.setText(tr("deleting"))
        self.error_label.hide()

        try:
            auth = requests.post(
                f"{API_BASE}/login",
                json={"username": self.main_window.main_page.username, "password": admin_password},
                timeout=10,
            )
            if auth.status_code == 401:
                self._show_error(tr("err_wrong_admin_pass"))
                return
            if auth.status_code != 200:
                self._show_error(tr("err_verify_admin"))
                return

            self.modify_btn.hide()
            self.cancel_btn.hide()
            self.delete_btn.hide()
            self.confirm_label.setText(tr("confirm_delete_msg").format(self._current_username))
            self.confirm_frame.show()

        except requests.exceptions.ConnectionError:
            self._show_error(tr("err_connection"))
        except requests.exceptions.Timeout:
            self._show_error(tr("err_timeout"))
        except Exception:
            self._show_error(tr("err_unexpected_retry"))
        finally:
            self.delete_btn.setEnabled(True)
            self.delete_btn.setText(tr("delete_user_btn"))

    def _do_delete(self):
        self.confirm_yes_btn.setEnabled(False)
        self.confirm_yes_btn.setText(tr("deleting"))
        self.error_label.hide()

        try:
            response = requests.delete(
                f"{API_BASE}/users/delete/{self.user_id}",
                params={"token": self.main_window.access_token},
                timeout=10,
            )
            if response.status_code == 200:
                self.main_window.go_to_user_list()
            elif response.status_code == 404:
                self._show_error(tr("err_user_not_found"))
                self._cancel_confirm()
            else:
                self._show_error(tr("err_server").format(response.status_code))
                self._cancel_confirm()
        except requests.exceptions.ConnectionError:
            self._show_error(tr("err_connection"))
            self._cancel_confirm()
        except requests.exceptions.Timeout:
            self._show_error(tr("err_timeout"))
            self._cancel_confirm()
        except Exception:
            self._show_error(tr("err_unexpected_retry"))
            self._cancel_confirm()
        finally:
            self.confirm_yes_btn.setEnabled(True)
            self.confirm_yes_btn.setText(tr("confirm_delete_yes_btn"))

    def _cancel_confirm(self):
        self.confirm_frame.hide()
        self.modify_btn.show()
        self.cancel_btn.show()
        self.delete_btn.show()

    def _show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()
