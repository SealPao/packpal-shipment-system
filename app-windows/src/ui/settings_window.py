from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from services.settings_service import AppSettings, SettingsService
from ui.common import ScreenContainer, app_stylesheet, build_footer, create_card, create_page_header


class SettingsWindow(QMainWindow):
    def __init__(self, parent_window: QMainWindow | None = None, settings_service: SettingsService | None = None) -> None:
        super().__init__(parent_window)
        self.parent_window = parent_window
        self.settings_service = settings_service or SettingsService()
        self.setWindowTitle(f"{APP_TITLE} - 系統設定")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        settings = self.settings_service.load()

        container = ScreenContainer()
        self.setCentralWidget(container)

        card, card_layout = create_card()

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.operator_input = QLineEdit(settings.operator_name)
        self.operator_input.setPlaceholderText("例如：小包")

        self.nas_url_input = QLineEdit(settings.nas_url)
        self.nas_url_input.setPlaceholderText("例如：http://192.168.1.100:8000")

        self.storage_path_input = QLineEdit(settings.local_storage_path)
        self.storage_path_input.setPlaceholderText("本地儲存目錄")

        browse_button = QPushButton("選擇資料夾")
        browse_button.setObjectName("secondaryButton")
        browse_button.clicked.connect(self.choose_storage_path)

        storage_row = QHBoxLayout()
        storage_row.addWidget(self.storage_path_input, 1)
        storage_row.addWidget(browse_button)

        form.addRow("預設操作人員", self.operator_input)
        form.addRow("NAS API 位址", self.nas_url_input)
        form.addRow("本地儲存路徑", storage_row)

        hint = QLabel("相機裝置請在模式選擇頁設定，這裡先處理 NAS 與本地儲存設定。")
        hint.setObjectName("settingsHint")
        hint.setWordWrap(True)

        button_row = QHBoxLayout()
        save_button = QPushButton("儲存設定")
        save_button.clicked.connect(self.save_settings)
        back_button = QPushButton("返回")
        back_button.setObjectName("secondaryButton")
        back_button.clicked.connect(self.go_back)
        button_row.addWidget(save_button)
        button_row.addWidget(back_button)
        button_row.addStretch(1)

        card_layout.addLayout(form)
        card_layout.addWidget(hint)
        card_layout.addLayout(button_row)

        container.layout.addStretch(1)
        container.layout.addWidget(create_page_header("系統設定", "設定 NAS、預設操作人員與本地儲存路徑。"))
        container.layout.addWidget(card)
        container.layout.addStretch(1)
        container.layout.addWidget(build_footer())
        self.setStyleSheet(app_stylesheet())

    def choose_storage_path(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "選擇本地儲存資料夾", self.storage_path_input.text())
        if directory:
            self.storage_path_input.setText(directory)

    def save_settings(self) -> None:
        settings = AppSettings(
            operator_name=self.operator_input.text().strip(),
            nas_url=self.nas_url_input.text().strip(),
            local_storage_path=self.storage_path_input.text().strip(),
        )
        self.settings_service.save(settings)
        QMessageBox.information(self, "儲存完成", "系統設定已更新。")

    def go_back(self) -> None:
        if self.parent_window is not None:
            self.parent_window.show()
        self.close()