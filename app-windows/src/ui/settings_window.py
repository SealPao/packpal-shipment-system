from __future__ import annotations

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from services.employee_service import EmployeeService
from services.settings_service import AppSettings, SettingsService
from ui.common import ScreenContainer, app_stylesheet, apply_window_icon, build_footer, create_card, create_page_header


class SettingsWindow(QMainWindow):
    def __init__(self, parent_window: QMainWindow | None = None, settings_service: SettingsService | None = None, employee_service: EmployeeService | None = None) -> None:
        super().__init__(parent_window)
        self.parent_window = parent_window
        self.settings_service = settings_service or SettingsService()
        self.employee_service = employee_service or EmployeeService(self.settings_service)
        self.setWindowTitle(f"{APP_TITLE} - 系統設定")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        apply_window_icon(self)

        settings = self.settings_service.load()

        container = ScreenContainer()
        self.setCentralWidget(container)
        container.layout.setSpacing(16)

        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        back_button = QPushButton("返回")
        back_button.setObjectName("secondaryButton")
        back_button.clicked.connect(self.go_back)
        top_bar.addWidget(back_button)
        top_bar.addStretch(1)

        container.layout.addLayout(top_bar)
        container.layout.addWidget(create_page_header("系統設定", "先修正基本設定與員工匯入，細緻版 UI 之後再整理。", show_logo=False))

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(16)

        settings_card, settings_layout = create_card()
        settings_title = QLabel("連線與儲存")
        settings_title.setObjectName("sectionTitle")
        settings_layout.addWidget(settings_title)

        settings_hint = QLabel("先設定 NAS API 與本地儲存位置。相機選擇仍保留在模式選擇頁，避免作業時跟 webcam 打架。")
        settings_hint.setObjectName("settingsHint")
        settings_hint.setWordWrap(True)
        settings_layout.addWidget(settings_hint)

        self.nas_url_input = QLineEdit(settings.nas_url)
        self.nas_url_input.setPlaceholderText("例如：http://192.168.1.100:8000")
        settings_layout.addWidget(self._build_field_block("NAS API 位址", self.nas_url_input))

        self.storage_path_input = QLineEdit(settings.local_storage_path)
        self.storage_path_input.setPlaceholderText("選擇本地暫存與草稿儲存位置")
        browse_button = QPushButton("選擇資料夾")
        browse_button.setObjectName("secondaryButton")
        browse_button.clicked.connect(self.choose_storage_path)

        storage_widget = QWidget()
        storage_row = QHBoxLayout(storage_widget)
        storage_row.setContentsMargins(0, 0, 0, 0)
        storage_row.setSpacing(12)
        storage_row.addWidget(self.storage_path_input, 1)
        storage_row.addWidget(browse_button)
        settings_layout.addWidget(self._build_field_block("本地儲存路徑", storage_widget))

        save_row = QHBoxLayout()
        save_row.setContentsMargins(0, 0, 0, 0)
        save_row.setSpacing(12)
        save_button = QPushButton("儲存設定")
        save_button.clicked.connect(self.save_settings)
        save_row.addWidget(save_button)
        save_row.addStretch(1)
        settings_layout.addLayout(save_row)

        employee_card, employee_layout = create_card()
        employee_title = QLabel("員工資料設定")
        employee_title.setObjectName("sectionTitle")
        employee_layout.addWidget(employee_title)

        employee_hint = QLabel("登入只輸入員工編號，名稱會自動帶出。支援 CSV 匯入；可先下載範例檔再填寫。")
        employee_hint.setObjectName("settingsHint")
        employee_hint.setWordWrap(True)
        employee_layout.addWidget(employee_hint)

        self.employee_file_label = QLabel()
        self.employee_file_label.setObjectName("settingsHint")
        self.employee_file_label.setWordWrap(True)
        employee_layout.addWidget(self.employee_file_label)

        employee_button_row = QHBoxLayout()
        employee_button_row.setContentsMargins(0, 0, 0, 0)
        employee_button_row.setSpacing(12)
        download_button = QPushButton("下載範例檔")
        download_button.setObjectName("secondaryButton")
        download_button.clicked.connect(self.download_sample_file)
        import_button = QPushButton("匯入員工檔")
        import_button.clicked.connect(self.import_employee_file)
        employee_button_row.addWidget(download_button)
        employee_button_row.addWidget(import_button)
        employee_button_row.addStretch(1)
        employee_layout.addLayout(employee_button_row)

        self.employee_table = QTableWidget(0, 2)
        self.employee_table.setHorizontalHeaderLabels(["員工編號", "員工名稱"])
        self.employee_table.verticalHeader().setVisible(False)
        self.employee_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.employee_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.employee_table.setAlternatingRowColors(True)
        self.employee_table.horizontalHeader().setStretchLastSection(True)
        self.employee_table.setMinimumHeight(260)
        employee_layout.addWidget(self.employee_table)

        self.employee_count_label = QLabel()
        self.employee_count_label.setObjectName("settingsHint")
        employee_layout.addWidget(self.employee_count_label)

        scroll_layout.addWidget(settings_card)
        scroll_layout.addWidget(employee_card)
        scroll_layout.addStretch(1)
        scroll_area.setWidget(scroll_content)

        container.layout.addWidget(scroll_area, 1)
        container.layout.addWidget(build_footer())
        self.setStyleSheet(app_stylesheet())
        self.refresh_employee_table()

    def closeEvent(self, event: QCloseEvent) -> None:
        app = QApplication.instance()
        if app is not None:
            app.quit()
        event.accept()

    def _build_field_block(self, label_text: str, field_widget: QWidget) -> QWidget:
        block = QWidget()
        layout = QVBoxLayout(block)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        label = QLabel(label_text)
        label.setObjectName("fieldLabel")
        layout.addWidget(label)
        layout.addWidget(field_widget)
        return block

    def choose_storage_path(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "選擇本地儲存資料夾", self.storage_path_input.text())
        if directory:
            self.storage_path_input.setText(directory)

    def save_settings(self) -> None:
        settings = AppSettings(
            nas_url=self.nas_url_input.text().strip(),
            local_storage_path=self.storage_path_input.text().strip(),
        )
        self.settings_service.save(settings)
        QMessageBox.information(self, "儲存完成", "系統設定已更新。")

    def download_sample_file(self) -> None:
        target_path, _ = QFileDialog.getSaveFileName(self, "下載員工範例檔", "packpal-employees-sample.csv", "CSV 檔案 (*.csv)")
        if not target_path:
            return
        self.employee_service.export_sample_csv(target_path)
        QMessageBox.information(self, "下載完成", f"員工範例檔已輸出到：\n{target_path}")

    def import_employee_file(self) -> None:
        source_path, _ = QFileDialog.getOpenFileName(self, "匯入員工檔", "", "CSV 檔案 (*.csv)")
        if not source_path:
            return

        try:
            count = self.employee_service.import_csv(source_path)
        except ValueError as error:
            QMessageBox.warning(self, "匯入失敗", str(error))
            return

        self.refresh_employee_table()
        QMessageBox.information(self, "匯入完成", f"已匯入 {count} 筆員工資料。")

    def refresh_employee_table(self) -> None:
        records = self.employee_service.load_records()
        self.employee_table.setRowCount(len(records))
        for row_index, record in enumerate(records):
            self.employee_table.setItem(row_index, 0, QTableWidgetItem(record.employee_id))
            self.employee_table.setItem(row_index, 1, QTableWidgetItem(record.name))
        self.employee_count_label.setText(f"目前員工資料筆數：{len(records)}")
        self.employee_file_label.setText(f"目前員工檔：{self.employee_service.employee_file_path()}")

    def go_back(self) -> None:
        if self.parent_window is not None:
            self.parent_window.show()
        self.hide()
