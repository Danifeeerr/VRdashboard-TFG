import requests
from datetime import date

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QGridLayout
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
CARD_BG = "#F5E1CE"


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


class AssignationPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.user = None
        self._cached_trainings = []
        self.setStyleSheet(f"background-color: {WHITE};")
        self._build_ui()

    def set_user(self, user):
        self.user = user
        self.title_label.setText(tr("assign_title_named").format(user["username"]))
        self.load_trainings()

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

        self.btn_back = HoverButton(tr("user_list_btn_back"))
        self.btn_back.setFixedSize(150, 40)
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        font_btn = QFont()
        font_btn.setPointSize(10)
        font_btn.setBold(True)
        self.btn_back.setFont(font_btn)
        self.btn_back.clicked.connect(self.main_window.go_to_user_list)
        layout.addWidget(self.btn_back)

        return header

    def _body(self):
        body = QFrame()
        body.setStyleSheet(f"background-color: {WHITE};")

        outer = QVBoxLayout(body)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(16)

        self.title_label = QLabel(tr("assign_title"))
        font_title = QFont()
        font_title.setPointSize(10)
        font_title.setBold(True)
        self.title_label.setFont(font_title)
        self.title_label.setStyleSheet(f"color: {DARK_TEXT};")
        outer.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.msg_label = QLabel("")
        font_msg = QFont()
        font_msg.setPointSize(9)
        self.msg_label.setFont(font_msg)
        self.msg_label.setStyleSheet("color: #D9534F; background: transparent;")
        self.msg_label.hide()
        outer.addWidget(self.msg_label, alignment=Qt.AlignmentFlag.AlignLeft)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        self.cards_container = QWidget()
        self.cards_container.setStyleSheet(f"background: {WHITE};")
        self.grid_layout = QGridLayout(self.cards_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        scroll.setWidget(self.cards_container)
        outer.addWidget(scroll, stretch=1)

        return body

    def load_trainings(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.msg_label.hide()

        try:
            response = requests.get(f"{API_BASE}/training", timeout=10)
            if response.status_code != 200:
                return
            trainings = response.json()
        except Exception:
            return

        self._cached_trainings = trainings
        cols = 4
        for i, training in enumerate(trainings):
            card = self._build_card(training)
            self.grid_layout.addWidget(card, i // cols, i % cols)

    def _build_card(self, training):
        card = QFrame()
        card.setFixedSize(180, 160)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {CARD_BG};
                border-radius: 6px;
                border: 1px solid {LIGHT_BORDER};
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        font_name = QFont()
        font_name.setPointSize(11)
        font_name.setBold(True)

        font_info = QFont()
        font_info.setPointSize(8)

        lbl_name = QLabel(training["name"])
        lbl_name.setFont(font_name)
        lbl_name.setStyleSheet(f"color: {DARK_TEXT}; border: none;")
        lbl_name.setWordWrap(True)
        layout.addWidget(lbl_name)

        lbl_hours = QLabel(tr("approx_hours").format(training["hours"]))
        lbl_hours.setFont(font_info)
        lbl_hours.setStyleSheet(f"color: {DARK_TEXT}; border: none;")
        layout.addWidget(lbl_hours)

        lbl_errors = QLabel(tr("error_limit").format(training["error_limit"]))
        lbl_errors.setFont(font_info)
        lbl_errors.setStyleSheet(f"color: {DARK_TEXT}; border: none;")
        layout.addWidget(lbl_errors)

        layout.addStretch()

        font_btn = QFont()
        font_btn.setPointSize(11)
        font_btn.setBold(True)

        btn = HoverButton(tr("assign_btn"))
        btn.setFixedHeight(36)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(font_btn)
        btn.clicked.connect(lambda _, t=training: self.handle_assign(t))
        layout.addWidget(btn)

        return card

    def handle_assign(self, training):
        if not self.user:
            return

        try:
            response = requests.post(
                f"{API_BASE}/assignation/new",
                json={
                    "userid": self.user["id"],
                    "trainingid": training["id"],
                    "date": date.today().isoformat(),
                },
                timeout=10,
            )
            if response.status_code == 200:
                self._show_msg(tr("success_assigned").format(training["name"]), success=True)
            elif response.status_code == 409:
                self._show_msg(tr("err_already_assigned"))
            else:
                self._show_msg(tr("err_server").format(response.status_code))
        except requests.exceptions.ConnectionError:
            self._show_msg(tr("err_connection"))
        except requests.exceptions.Timeout:
            self._show_msg(tr("err_timeout"))
        except Exception:
            self._show_msg(tr("err_unexpected"))

    def retranslate_ui(self):
        self.header_title.setText(tr("app_title"))
        self.btn_back.setText(tr("user_list_btn_back"))
        if self.user:
            self.title_label.setText(tr("assign_title_named").format(self.user["username"]))
        else:
            self.title_label.setText(tr("assign_title"))
        self.msg_label.hide()
        self._rebuild_cards()

    def _rebuild_cards(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        cols = 4
        for i, training in enumerate(self._cached_trainings):
            card = self._build_card(training)
            self.grid_layout.addWidget(card, i // cols, i % cols)

    def _show_msg(self, text, success=False):
        color = "#5CB85C" if success else "#D9534F"
        self.msg_label.setStyleSheet(f"color: {color}; background: transparent;")
        self.msg_label.setText(text)
        self.msg_label.show()
