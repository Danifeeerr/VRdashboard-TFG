import requests
from datetime import date

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QGridLayout
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
        self.setStyleSheet(f"background-color: {WHITE};")
        self._build_ui()

    def set_user(self, user):
        self.user = user
        self.title_label.setText(f"Assigna un entrenament per a l'usuari ({user['username']})")
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

        title = QLabel("Programa de monitorament")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_title = QFont()
        font_title.setPointSize(18)
        font_title.setBold(True)
        title.setFont(font_title)
        title.setStyleSheet(f"color: {WHITE}; background: transparent;")
        layout.addWidget(title, stretch=1)

        btn_back = HoverButton("Llista d'usuaris")
        btn_back.setFixedSize(150, 40)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        font_btn = QFont()
        font_btn.setPointSize(10)
        font_btn.setBold(True)
        btn_back.setFont(font_btn)
        btn_back.clicked.connect(self.main_window.go_to_user_list)
        layout.addWidget(btn_back)

        return header

    def _body(self):
        body = QFrame()
        body.setStyleSheet(f"background-color: {WHITE};")

        outer = QVBoxLayout(body)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(16)

        self.title_label = QLabel("Assigna un entrenament per a l'usuari")
        font_title = QFont()
        font_title.setPointSize(10)
        font_title.setBold(True)
        self.title_label.setFont(font_title)
        self.title_label.setStyleSheet(f"color: {DARK_TEXT};")
        outer.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Missatge d'error/èxit
        self.msg_label = QLabel("")
        font_msg = QFont()
        font_msg.setPointSize(9)
        self.msg_label.setFont(font_msg)
        self.msg_label.setStyleSheet("color: #D9534F; background: transparent;")
        self.msg_label.hide()
        outer.addWidget(self.msg_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Scroll amb les targetes
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
        # Netejar grid
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

        lbl_hours = QLabel(f"Hores aproximades: {training['hours']}")
        lbl_hours.setFont(font_info)
        lbl_hours.setStyleSheet(f"color: {DARK_TEXT}; border: none;")
        layout.addWidget(lbl_hours)

        lbl_errors = QLabel(f"Límit d'errors: {training['error_limit']}")
        lbl_errors.setFont(font_info)
        lbl_errors.setStyleSheet(f"color: {DARK_TEXT}; border: none;")
        layout.addWidget(lbl_errors)

        layout.addStretch()

        font_btn = QFont()
        font_btn.setPointSize(11)
        font_btn.setBold(True)

        btn = HoverButton("Assignar")
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
                self._show_msg(f"Entrenament '{training['name']}' assignat correctament.", success=True)
            elif response.status_code == 409:
                self._show_msg("Aquest usuari ja té aquest entrenament assignat.")
            else:
                self._show_msg(f"Error del servidor ({response.status_code}).")
        except requests.exceptions.ConnectionError:
            self._show_msg("No s'ha pogut connectar amb el servidor.")
        except requests.exceptions.Timeout:
            self._show_msg("El servidor no ha respost a temps.")
        except Exception:
            self._show_msg("Error inesperat.")

    def _show_msg(self, text, success=False):
        color = "#5CB85C" if success else "#D9534F"
        self.msg_label.setStyleSheet(f"color: {color}; background: transparent;")
        self.msg_label.setText(text)
        self.msg_label.show()
