from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from ui.common import ScreenContainer, build_footer
from ui.mode_select_window import ModeSelectWindow


class LoginWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.mode_window: ModeSelectWindow | None = None

        self.setWindowTitle(f"{APP_TITLE} - 登入")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        container = ScreenContainer()
        self.setCentralWidget(container)

        title = QLabel("PackPal Shipment System")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("請登入系統以開始作業")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("請輸入帳號")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("請輸入密碼")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form.addRow("帳號", self.username_input)
        form.addRow("密碼", self.password_input)

        action_row = QHBoxLayout()
        action_row.addStretch(1)

        self.login_button = QPushButton("登入")
        self.login_button.setMinimumHeight(42)
        self.login_button.clicked.connect(self.handle_login)
        action_row.addWidget(self.login_button)

        card_layout.addLayout(form)
        card_layout.addLayout(action_row)

        container.layout.addStretch(1)
        container.layout.addWidget(title)
        container.layout.addWidget(subtitle)
        container.layout.addWidget(card)
        container.layout.addStretch(1)
        container.layout.addWidget(build_footer())

        self.setStyleSheet(_build_stylesheet())

    def handle_login(self) -> None:
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "登入失敗", "請輸入帳號與密碼。")
            return

        self.mode_window = ModeSelectWindow(parent_login=self)
        self.mode_window.show()
        self.hide()



def _build_stylesheet() -> str:
    return """
        QMainWindow {
            background-color: #f5f7fb;
        }
        #screenContainer {
            background-color: #f5f7fb;
        }
        #pageTitle {
            font-size: 28px;
            font-weight: 700;
            color: #1f2937;
        }
        #pageSubtitle {
            font-size: 15px;
            color: #4b5563;
        }
        #card {
            background-color: white;
            border: 1px solid #dbe2ea;
            border-radius: 16px;
        }
        QLabel {
            color: #111827;
        }
        QLineEdit {
            min-height: 38px;
            padding: 6px 10px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            background-color: #ffffff;
        }
        QPushButton {
            padding: 10px 18px;
            border: none;
            border-radius: 10px;
            background-color: #2563eb;
            color: white;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: #1d4ed8;
        }
        #footerLabel {
            font-size: 12px;
            color: #6b7280;
        }
    """
