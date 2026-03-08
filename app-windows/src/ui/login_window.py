from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QVBoxLayout

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from services.employee_service import EmployeeRecord, EmployeeService
from services.settings_service import SettingsService
from ui.common import ScreenContainer, app_stylesheet, apply_window_icon, build_footer, create_card, create_page_header
from ui.mode_select_window import ModeSelectWindow
from ui.settings_window import SettingsWindow


class LoginWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.mode_window: ModeSelectWindow | None = None
        self.settings_window: SettingsWindow | None = None
        self.settings_service = SettingsService()
        self.employee_service = EmployeeService(self.settings_service)
        self.current_employee: EmployeeRecord | None = None

        self.setWindowTitle(f"{APP_TITLE} - 進入作業")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        apply_window_icon(self)

        container = ScreenContainer()
        self.setCentralWidget(container)

        card, card_layout = create_card()

        self.employee_id_input = QLineEdit()
        self.employee_id_input.setPlaceholderText("請輸入員工編號")
        self.employee_id_input.textChanged.connect(self.handle_employee_id_changed)

        self.employee_name_label = QLabel("員工名稱會在輸入正確編號後自動帶出")
        self.employee_name_label.setObjectName("employeeStatus")
        self.employee_name_label.setWordWrap(True)

        self.employee_status_label = QLabel("請先輸入員工編號；若沒有資料，請先到系統設定匯入員工檔。")
        self.employee_status_label.setObjectName("employeeStatus")
        self.employee_status_label.setWordWrap(True)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        employee_id_label = QLabel("員工編號")
        employee_id_label.setObjectName("fieldLabel")
        form_layout.addWidget(employee_id_label)
        form_layout.addWidget(self.employee_id_input)

        employee_name_title = QLabel("員工名稱")
        employee_name_title.setObjectName("fieldLabel")
        form_layout.addWidget(employee_name_title)
        form_layout.addWidget(self.employee_name_label)

        help_title = QLabel("說明")
        help_title.setObjectName("fieldLabel")
        form_layout.addWidget(help_title)
        form_layout.addWidget(self.employee_status_label)

        action_row = QHBoxLayout()
        settings_button = QPushButton("系統設定")
        settings_button.setObjectName("secondaryButton")
        settings_button.clicked.connect(self.open_settings)

        enter_button = QPushButton("進入作業")
        enter_button.clicked.connect(self.handle_enter)

        action_row.addWidget(settings_button)
        action_row.addStretch(1)
        action_row.addWidget(enter_button)

        card_layout.addLayout(form_layout)
        card_layout.addLayout(action_row)

        container.layout.addStretch(1)
        container.layout.addWidget(create_page_header("出貨小幫手", "請輸入員工編號，系統會自動帶出名稱後再進入作業。"))
        container.layout.addWidget(card)
        container.layout.addStretch(1)
        container.layout.addWidget(build_footer())

        self.setStyleSheet(app_stylesheet())

    def handle_employee_id_changed(self) -> None:
        employee_id = self.employee_id_input.text().strip()
        employee = self.employee_service.find_by_id(employee_id)
        self.current_employee = employee

        if employee is None:
            self.employee_name_label.setText("員工名稱會在輸入正確編號後自動帶出")
            if employee_id:
                self.employee_status_label.setText("查無此員工編號，請確認後再進入作業。")
            else:
                self.employee_status_label.setText("請先輸入員工編號；若沒有資料，請先到系統設定匯入員工檔。")
            return

        self.employee_name_label.setText(employee.name)
        self.employee_status_label.setText(f"已帶出員工：{employee.employee_id} / {employee.name}")

    def handle_enter(self) -> None:
        employee_id = self.employee_id_input.text().strip()
        if not employee_id:
            QMessageBox.warning(self, "資料不足", "請先輸入員工編號。")
            return

        employee = self.employee_service.find_by_id(employee_id)
        if employee is None:
            QMessageBox.warning(self, "查無員工", "找不到這個員工編號，請先到系統設定匯入員工資料。")
            return

        self.current_employee = employee
        self.mode_window = ModeSelectWindow(parent_login=self, current_employee=employee)
        self.mode_window.show()
        self.hide()

    def open_settings(self) -> None:
        self.settings_window = SettingsWindow(parent_window=self, settings_service=self.settings_service, employee_service=self.employee_service)
        self.settings_window.show()
        self.hide()
