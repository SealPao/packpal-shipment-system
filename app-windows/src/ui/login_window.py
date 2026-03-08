from __future__ import annotations

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QVBoxLayout

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
        card_layout.setSpacing(18)

        prompt_label = QLabel("員工號碼")
        prompt_label.setObjectName("fieldLabel")

        self.employee_id_input = QLineEdit()
        self.employee_id_input.setObjectName("heroInput")
        self.employee_id_input.setPlaceholderText("請輸入員工編號")
        self.employee_id_input.textChanged.connect(self.handle_employee_id_changed)
        self.employee_id_input.returnPressed.connect(self.handle_enter)

        self.employee_name_label = QLabel("尚未帶出員工名稱")
        self.employee_name_label.setObjectName("heroName")
        self.employee_name_label.setWordWrap(True)

        self.enter_button = QPushButton("請點我開始工作")
        self.enter_button.setMinimumHeight(72)
        self.enter_button.clicked.connect(self.handle_enter)

        helper_label = QLabel("若查不到員工，請到系統設定編輯或匯入員工資料。")
        helper_label.setObjectName("employeeStatus")
        helper_label.setWordWrap(True)

        card_layout.addWidget(prompt_label)
        card_layout.addWidget(self.employee_id_input)
        card_layout.addWidget(self.employee_name_label)
        card_layout.addWidget(self.enter_button)
        card_layout.addWidget(helper_label)

        action_row = QHBoxLayout()
        settings_button = QPushButton("系統設定")
        settings_button.setObjectName("secondaryButton")
        settings_button.clicked.connect(self.open_settings)
        action_row.addWidget(settings_button)
        action_row.addStretch(1)
        card_layout.addLayout(action_row)

        container.layout.addStretch(1)
        container.layout.addWidget(create_page_header("出貨小幫手", "輸入員工號碼後，系統會自動帶出姓名。"))
        container.layout.addWidget(card)
        container.layout.addStretch(1)
        container.layout.addWidget(build_footer())

        self.setStyleSheet(app_stylesheet())

    def closeEvent(self, event: QCloseEvent) -> None:
        app = QApplication.instance()
        if app is not None:
            app.quit()
        event.accept()

    def handle_employee_id_changed(self) -> None:
        employee_id = self.employee_id_input.text().strip()
        employee = self.employee_service.find_by_id(employee_id)
        self.current_employee = employee

        if employee is None:
            self.employee_name_label.setText("尚未帶出員工名稱")
            if employee_id:
                self.enter_button.setText("查無員工，請先修正資料")
            else:
                self.enter_button.setText("請點我開始工作")
            return

        self.employee_name_label.setText(f"歡迎尊貴的 {employee.employee_id} {employee.name}")
        self.enter_button.setText(f"歡迎尊貴的 {employee.employee_id} {employee.name}，請點我開始工作")

    def handle_enter(self) -> None:
        employee_id = self.employee_id_input.text().strip()
        if not employee_id:
            QMessageBox.warning(self, "資料不足", "請先輸入員工編號。")
            return

        employee = self.employee_service.find_by_id(employee_id)
        if employee is None:
            QMessageBox.warning(self, "查無員工", "找不到這個員工編號，請先到系統設定匯入或編輯員工資料。")
            return

        self.current_employee = employee
        self.mode_window = ModeSelectWindow(parent_login=self, current_employee=employee)
        self.mode_window.show()
        self.hide()

    def open_settings(self) -> None:
        self.settings_window = SettingsWindow(parent_window=self, settings_service=self.settings_service, employee_service=self.employee_service)
        self.settings_window.show()
        self.hide()
