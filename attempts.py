import requests

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QScrollArea
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


class AttemptsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.user = None
        self._training_cache = {}
        self._assignation_cache = {}
        self.setStyleSheet(f"background-color: {WHITE};")
        self._build_ui()

    def set_user(self, user):
        self.user = user
        self._training_cache = {}
        self._assignation_cache = {}
        self.title_label.setText(f"Intents de  ({user['username']})")
        self.date_filter_input.clear()
        self.load_attempts()

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
        outer.setSpacing(12)

        # Títol
        self.title_label = QLabel("Intents de")
        font_title = QFont()
        font_title.setPointSize(10)
        font_title.setBold(True)
        self.title_label.setFont(font_title)
        self.title_label.setStyleSheet(f"color: {DARK_TEXT};")
        outer.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Filtre per data
        filter_frame = QFrame()
        filter_frame.setStyleSheet(f"border: 1px solid {LIGHT_BORDER}; border-radius: 4px; background: {WHITE};")
        filter_frame.setFixedHeight(50)
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(12, 0, 12, 0)
        filter_layout.setSpacing(12)

        lbl_data = QLabel("Data de l'intent")
        lbl_data.setStyleSheet(f"color: {DARK_TEXT}; border: none;")
        font_lbl = QFont()
        font_lbl.setPointSize(9)
        lbl_data.setFont(font_lbl)

        self.date_filter_input = QLineEdit()
        self.date_filter_input.setPlaceholderText("dd/mm/aaaa")
        self.date_filter_input.setFixedSize(140, 30)
        self.date_filter_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {LIGHT_BORDER};
                border-radius: 4px;
                padding: 0 8px;
                font-size: 12px;
                color: {DARK_TEXT};
                background: {WHITE};
            }}
        """)

        btn_cerca = HoverButton("Cerca")
        btn_cerca.setFixedSize(90, 34)
        btn_cerca.setCursor(Qt.CursorShape.PointingHandCursor)
        font_btn2 = QFont()
        font_btn2.setPointSize(10)
        font_btn2.setBold(True)
        btn_cerca.setFont(font_btn2)
        btn_cerca.clicked.connect(self.load_attempts)

        filter_layout.addWidget(lbl_data)
        filter_layout.addWidget(self.date_filter_input)
        filter_layout.addWidget(btn_cerca)
        filter_layout.addStretch()

        outer.addWidget(filter_frame)

        # Scroll amb la llista d'intents
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

    def load_attempts(self):
        if not self.user:
            return

        date_filter = self.date_filter_input.text().strip()

        try:
            response = requests.get(
                f"{API_BASE}/attempt/user",
                params={"userid": self.user["id"]},
                timeout=10,
            )
            if response.status_code == 404:
                self._clear_list()
                return
            if response.status_code != 200:
                return
            attempts = response.json()
        except Exception:
            return

        # Filtre per data (format dd/mm/aaaa → yyyy-mm-dd)
        if date_filter:
            try:
                day, month, year = date_filter.split("/")
                date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                attempts = [a for a in attempts if a["timestamp"].startswith(date_str)]
            except ValueError:
                pass

        # Carregar assignacions de l'usuari (per "prèviament completat")
        self._load_assignation_cache()

        self._clear_list()
        for attempt in attempts:
            training = self._get_training(attempt["trainingid"])
            row = self._build_row(attempt, training)
            self.list_layout.insertWidget(self.list_layout.count() - 1, row)

    def _load_assignation_cache(self):
        try:
            response = requests.get(
                f"{API_BASE}/assignation/{self.user['id']}",
                timeout=10,
            )
            if response.status_code == 200:
                for a in response.json():
                    self._assignation_cache[a["trainingid"]] = a
        except Exception:
            pass

    def _get_training(self, training_id):
        if training_id in self._training_cache:
            return self._training_cache[training_id]
        try:
            response = requests.get(f"{API_BASE}/training/{training_id}", timeout=10)
            if response.status_code == 200:
                training = response.json()
                self._training_cache[training_id] = training
                return training
        except Exception:
            pass
        return None

    def _build_row(self, attempt, training):
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
        layout.setSpacing(16)

        font_row = QFont()
        font_row.setPointSize(8)
        font_row.setBold(True)

        timestamp = attempt["timestamp"]
        try:
            date_part = timestamp.split("T")[0]
            y, m, d = date_part.split("-")
            data_str = f"{d}/{m}/{y}"
        except Exception:
            data_str = timestamp

        training_name = training["name"] if training else f"ID {attempt['trainingid']}"
        error_limit = training["error_limit"] if training else None

        assignation = self._assignation_cache.get(attempt["trainingid"])
        prev_completat = "Sí" if assignation and assignation.get("completed") else "No"

        if error_limit is not None:
            aprovat = "Sí" if attempt["number_errors"] <= error_limit else "No"
        else:
            aprovat = "?"

        def make_label(text):
            lbl = QLabel(text)
            lbl.setFont(font_row)
            lbl.setStyleSheet(f"color: {DARK_TEXT};")
            return lbl

        layout.addWidget(make_label(f"Data: {data_str}"))
        layout.addWidget(make_label(f"Entrenament: {training_name}"))
        layout.addWidget(make_label(f"Prèviament completat: {prev_completat}"))
        layout.addWidget(make_label(f"Temps emprat en hores: {attempt['time_spent']}"))
        layout.addWidget(make_label(f"Número d'errors: {attempt['number_errors']}"))
        layout.addWidget(make_label(f"Aprovat: {aprovat}"))
        layout.addStretch()

        btn_eliminar = HoverButton("Eliminar")
        btn_eliminar.setFixedSize(90, 36)
        btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_eliminar.setFont(font_row)
        btn_eliminar.clicked.connect(lambda _, a=attempt: self.handle_delete(a))
        layout.addWidget(btn_eliminar)

        return row

    def handle_delete(self, attempt):
        try:
            response = requests.delete(
                f"{API_BASE}/attempt/delete",
                params={
                    "userid": attempt["userid"],
                    "trainingid": attempt["trainingid"],
                    "timestamp": attempt["timestamp"],
                },
                timeout=10,
            )
            if response.status_code == 200:
                self.load_attempts()
        except Exception:
            pass

    def _clear_list(self):
        while self.list_layout.count() > 1:
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
