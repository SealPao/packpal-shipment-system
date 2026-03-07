from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from ui.common import ScreenContainer, app_stylesheet, build_footer, create_card, create_page_header
from ui.mode_select_window import ModeSelectWindow


class LoginWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.mode_window: ModeSelectWindow | None = None

        self.setWindowTitle(f"{APP_TITLE} - 登入")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        container = ScreenContainer()
        self.setCentralWidget(container)

        card, card_layout = create_card()

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
        container.layout.addWidget(create_page_header("PackPal Shipment System", "請登入系統以開始作業"))
        container.layout.addWidget(card)
        container.layout.addStretch(1)
        container.layout.addWidget(build_footer())

        self.setStyleSheet(app_stylesheet())

    def handle_login(self) -> None:
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "登入失敗", "請輸入帳號與密碼。")
            return

        self.mode_window = ModeSelectWindow(parent_login=self)
        self.mode_window.show()
        self.hide()