import requests

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QCheckBox, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from config import API_BASE
from translations import tr

ORANGE = "#F58953"
WHITE = "#FFFFFF"
YELLOW = "#FFC046"
HOVER_COLOR = "#F5A453"
DARK_TEXT = "#2C2C2A"
LIGHT_BORDER = "#CCCCCC"
ROW_BG = "#F5E1CE"


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
        self._cached_users = []
        self.setStyleSheet(f"background-color: {WHITE};")
        self._build_ui()

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

        self.btn_back = HoverButton(tr("main_page_btn"))
        self.btn_back.setFixedSize(150, 40)
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        font_btn = QFont()
        font_btn.setPointSize(10)
        font_btn.setBold(True)
        self.btn_back.setFont(font_btn)
        self.btn_back.clicked.connect(self.main_window.go_to_main_page)
        layout.addWidget(self.btn_back)

        return header

    def _body(self):
        body = QFrame()
        body.setStyleSheet(f"background-color: {WHITE};")

        outer = QVBoxLayout(body)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(12)

        self.lbl_filtre = QLabel(tr("user_filter_title"))
        font_filtre = QFont()
        font_filtre.setPointSize(10)
        font_filtre.setBold(True)
        self.lbl_filtre.setFont(font_filtre)
        self.lbl_filtre.setStyleSheet(f"color: {DARK_TEXT};")
        outer.addWidget(self.lbl_filtre, alignment=Qt.AlignmentFlag.AlignLeft)

        filter_frame = QFrame()
        filter_frame.setStyleSheet(f"border: 1px solid {LIGHT_BORDER}; border-radius: 4px; background: {WHITE};")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(12, 8, 12, 8)
        filter_layout.setSpacing(12)

        self.lbl_nom = QLabel(tr("username_filter_label"))
        self.lbl_nom.setStyleSheet(f"color: {DARK_TEXT}; border: none;")
        font_lbl = QFont()
        font_lbl.setPointSize(9)
        self.lbl_nom.setFont(font_lbl)

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

        self.lbl_admin_filter = QLabel(tr("admin_filter_label"))
        self.lbl_admin_filter.setStyleSheet(f"color: {DARK_TEXT}; border: none;")
        self.lbl_admin_filter.setFont(font_lbl)

        self.filter_admin_check = QCheckBox()
        self.filter_admin_check.setStyleSheet("border: none;")

        self.btn_cerca = HoverButton(tr("search_btn"))
        self.btn_cerca.setFixedSize(90, 34)
        self.btn_cerca.setCursor(Qt.CursorShape.PointingHandCursor)
        font_btn = QFont()
        font_btn.setPointSize(10)
        font_btn.setBold(True)
        self.btn_cerca.setFont(font_btn)
        self.btn_cerca.clicked.connect(self.load_users)

        filter_layout.addWidget(self.lbl_nom)
        filter_layout.addWidget(self.filter_input)
        filter_layout.addWidget(self.lbl_admin_filter)
        filter_layout.addWidget(self.filter_admin_check)
        filter_layout.addWidget(self.btn_cerca)
        filter_layout.addStretch()

        outer.addWidget(filter_frame)

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

        if username_filter:
            users = [u for u in users if username_filter in u["username"].lower()]
        if admin_filter:
            users = [u for u in users if u["admin"]]

        self._cached_users = []
        while self.list_layout.count() > 1:
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for user in users:
            count = self._get_assignation_count(user["id"])
            self._cached_users.append((user, count))
            row = self._build_user_row(user, count)
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

        admin_text = tr("yes") if user["admin"] else tr("no")

        lbl_username = QLabel(user["username"])
        lbl_username.setFont(font_row)
        lbl_username.setStyleSheet(f"color: {DARK_TEXT};")
        lbl_username.setFixedWidth(150)

        lbl_admin = QLabel(tr("admin_col").format(admin_text))
        lbl_admin.setFont(font_row)
        lbl_admin.setStyleSheet(f"color: {DARK_TEXT};")
        lbl_admin.setFixedWidth(160)

        lbl_assignacions = QLabel(tr("assigned_trainings_col").format(assignation_count))
        lbl_assignacions.setFont(font_row)
        lbl_assignacions.setStyleSheet(f"color: {DARK_TEXT};")

        font_btn = QFont()
        font_btn.setPointSize(10)
        font_btn.setBold(True)

        btn_intents = HoverButton(tr("attempts_btn"))
        btn_intents.setFixedSize(90, 36)
        btn_intents.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_intents.setFont(font_btn)
        btn_intents.clicked.connect(lambda _, u=user: self.main_window.go_to_attempts(u))

        btn_assignar = HoverButton(tr("assign_training_btn"))
        btn_assignar.setFixedSize(180, 36)
        btn_assignar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_assignar.setFont(font_btn)
        btn_assignar.clicked.connect(lambda _, u=user: self.main_window.go_to_assignation(u))

        btn_modificar = HoverButton(tr("modify_btn"))
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

    def retranslate_ui(self):
        self.header_title.setText(tr("app_title"))
        self.btn_back.setText(tr("main_page_btn"))
        self.lbl_filtre.setText(tr("user_filter_title"))
        self.lbl_nom.setText(tr("username_filter_label"))
        self.lbl_admin_filter.setText(tr("admin_filter_label"))
        self.btn_cerca.setText(tr("search_btn"))
        self._rebuild_rows()

    def _rebuild_rows(self):
        while self.list_layout.count() > 1:
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for user, count in self._cached_users:
            row = self._build_user_row(user, count)
            self.list_layout.insertWidget(self.list_layout.count() - 1, row)
