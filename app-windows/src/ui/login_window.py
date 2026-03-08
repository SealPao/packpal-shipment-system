from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QLineEdit, QMainWindow, QMessageBox, QPushButton

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from services.settings_service import SettingsService
from ui.common import ScreenContainer, app_stylesheet, build_footer, create_card, create_page_header
from ui.mode_select_window import ModeSelectWindow
from ui.settings_window import SettingsWindow


class LoginWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.mode_window: ModeSelectWindow | None = None
        self.settings_window: SettingsWindow | None = None
        self.settings_service = SettingsService()

        self.setWindowTitle(f"{APP_TITLE} - 進入作業")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        container = ScreenContainer()
        self.setCentralWidget(container)

        card, card_layout = create_card()

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        saved_settings = self.settings_service.load()
        self.operator_input = QLineEdit(saved_settings.operator_name)
        self.operator_input.setPlaceholderText("請輸入操作人員名稱")

        form.addRow("操作人員", self.operator_input)

        action_row = QHBoxLayout()
        settings_button = QPushButton("系統設定")
        settings_button.setObjectName("secondaryButton")
        settings_button.clicked.connect(self.open_settings)

        enter_button = QPushButton("進入作業")
        enter_button.clicked.connect(self.handle_enter)

        action_row.addWidget(settings_button)
        action_row.addStretch(1)
        action_row.addWidget(enter_button)

        card_layout.addLayout(form)
        card_layout.addLayout(action_row)

        container.layout.addStretch(1)
        container.layout.addWidget(create_page_header("出貨小幫手", "輸入操作人員名稱後即可開始，不需要密碼。"))
        container.layout.addWidget(card)
        container.layout.addStretch(1)
        container.layout.addWidget(build_footer())

        self.setStyleSheet(app_stylesheet())

    def handle_enter(self) -> None:
        operator_name = self.operator_input.text().strip()
        if not operator_name:
            QMessageBox.warning(self, "資料不足", "請先輸入操作人員名稱。")
            return

        current = self.settings_service.load()
        self.settings_service.save(current.__class__(
            operator_name=operator_name,
            nas_url=current.nas_url,
            local_storage_path=current.local_storage_path,
        ))

        self.mode_window = ModeSelectWindow(parent_login=self)
        self.mode_window.show()
        self.hide()

    def open_settings(self) -> None:
        self.settings_window = SettingsWindow(parent_window=self, settings_service=self.settings_service)
        self.settings_window.show()
        self.hide()