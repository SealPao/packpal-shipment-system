from __future__ import annotations

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QComboBox, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from services.camera_service import CameraOption, CameraService
from services.draft_service import DraftService
from services.employee_service import EmployeeRecord, EmployeeService
from services.settings_service import SettingsService
from ui.common import ScreenContainer, app_stylesheet, apply_window_icon, build_footer, create_card, create_mode_button, create_split_header, show_window_like
from ui.repair_receiving_window import RepairReceivingWindow
from ui.return_receiving_window import ReturnReceivingWindow
from ui.settings_window import SettingsWindow
from ui.shipment_window import ShipmentWindow


class ModeSelectWindow(QMainWindow):
    def __init__(self, parent_login: QMainWindow | None = None, current_employee: EmployeeRecord | None = None, camera_service: CameraService | None = None, draft_service: DraftService | None = None) -> None:
        super().__init__(parent_login)
        self.parent_login = parent_login
        self.current_employee = current_employee
        self.child_window: QMainWindow | None = None
        self.settings_window: SettingsWindow | None = None
        self.camera_service = camera_service or CameraService()
        self.draft_service = draft_service or DraftService()
        self.settings_service = SettingsService()
        self.employee_service = EmployeeService(self.settings_service)
        self.cameras: list[CameraOption] = []

        self.setWindowTitle(f"{APP_TITLE} - 模式選擇")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        apply_window_icon(self)

        container = ScreenContainer()
        self.setCentralWidget(container)

        container.layout.addWidget(create_split_header("選擇作業模式", "請直接選擇要進行的作業。"))

        card, card_layout = create_card()
        card_layout.setSpacing(20)

        operator_label = QLabel(self._operator_text())
        operator_label.setObjectName("cameraStatus")
        card_layout.addWidget(operator_label)

        mode_row = QHBoxLayout()
        mode_row.setSpacing(20)
        shipment_button = create_mode_button("出貨作業")
        repair_button = create_mode_button("維修收貨")
        return_button = create_mode_button("退貨收貨")
        shipment_button.clicked.connect(lambda: self.open_child_window(ShipmentWindow(self, self.selected_camera_name(), self.draft_service)))
        repair_button.clicked.connect(lambda: self.open_child_window(RepairReceivingWindow(self, self.selected_camera_name(), self.draft_service)))
        return_button.clicked.connect(lambda: self.open_child_window(ReturnReceivingWindow(self, self.selected_camera_name(), self.draft_service)))
        mode_row.addWidget(shipment_button, 1)
        mode_row.addWidget(repair_button, 1)
        mode_row.addWidget(return_button, 1)
        card_layout.addLayout(mode_row, 1)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(16)

        left_actions = QHBoxLayout()
        left_actions.setSpacing(12)
        settings_button = QPushButton("系統設定")
        settings_button.setObjectName("secondaryButton")
        settings_button.clicked.connect(self.open_settings)
        back_button = QPushButton("返回登入")
        back_button.setObjectName("secondaryButton")
        back_button.clicked.connect(self.go_back)
        left_actions.addWidget(settings_button)
        left_actions.addWidget(back_button)
        left_actions_widget = QWidget()
        left_actions_widget.setLayout(left_actions)

        camera_wrap = QWidget()
        camera_layout = QHBoxLayout(camera_wrap)
        camera_layout.setContentsMargins(0, 0, 0, 0)
        camera_layout.setSpacing(10)
        camera_label = QLabel("作業相機")
        camera_label.setObjectName("fieldLabel")
        self.camera_combo = QComboBox()
        self.camera_combo.setMinimumWidth(320)
        self.camera_combo.setMinimumHeight(48)
        self.camera_combo.currentIndexChanged.connect(self.persist_selected_camera)
        camera_layout.addWidget(camera_label)
        camera_layout.addWidget(self.camera_combo)

        bottom_row.addWidget(left_actions_widget)
        bottom_row.addStretch(1)
        bottom_row.addWidget(camera_wrap)
        card_layout.addLayout(bottom_row)

        container.layout.addWidget(card, 1)
        container.layout.addWidget(build_footer())

        self.refresh_camera_options()
        self.setStyleSheet(app_stylesheet("#0f766e", "#0d5f59"))

    def closeEvent(self, event: QCloseEvent) -> None:
        app = QApplication.instance()
        if app is not None:
            app.quit()
        event.accept()

    def _operator_text(self) -> str:
        if self.current_employee is None:
            return "目前尚未帶入操作人員。"
        return f"目前操作人員：{self.current_employee.employee_id} / {self.current_employee.name}"

    def refresh_camera_options(self) -> None:
        self.cameras = self.camera_service.list_cameras()
        selected_camera = self.camera_service.get_selected_camera(self.cameras)
        self.camera_combo.blockSignals(True)
        self.camera_combo.clear()
        if not self.cameras:
            self.camera_combo.addItem("沒有偵測到相機", "")
            self.camera_combo.setEnabled(False)
        else:
            self.camera_combo.setEnabled(True)
            for camera in self.cameras:
                self.camera_combo.addItem(camera.name, camera.id)
            selected_index = 0
            if selected_camera is not None:
                for index, camera in enumerate(self.cameras):
                    if camera.id == selected_camera.id:
                        selected_index = index
                        break
            self.camera_combo.setCurrentIndex(selected_index)
        self.camera_combo.blockSignals(False)

    def persist_selected_camera(self) -> None:
        camera_id = str(self.camera_combo.currentData())
        if camera_id:
            self.camera_service.save_selected_camera_id(camera_id)

    def selected_camera_name(self) -> str | None:
        camera_id = str(self.camera_combo.currentData())
        for camera in self.cameras:
            if camera.id == camera_id:
                return camera.name
        return None

    def open_settings(self) -> None:
        self.settings_window = SettingsWindow(parent_window=self, settings_service=self.settings_service, employee_service=self.employee_service)
        self.settings_window.show()
        self.hide()

    def open_child_window(self, window: QMainWindow) -> None:
        self.child_window = window
        self.child_window.show()
        self.hide()

    def go_back(self) -> None:
        if self.parent_login is not None:
            self.parent_login.show()
        self.hide()

