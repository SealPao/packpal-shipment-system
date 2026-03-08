from __future__ import annotations

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QLabel, QMainWindow, QPushButton

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from services.camera_service import CameraOption, CameraService
from services.draft_service import DraftService
from services.employee_service import EmployeeRecord, EmployeeService
from services.settings_service import SettingsService
from ui.common import ScreenContainer, app_stylesheet, apply_window_icon, build_footer, create_card, create_mode_button, create_page_header
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

        container.layout.addStretch(1)
        container.layout.addWidget(create_page_header("選擇作業模式", "請直接選擇要進行的作業；攝影機只在角落確認即可。"))

        card, card_layout = create_card()
        top_row = QHBoxLayout()
        operator_label = QLabel(self._operator_text())
        operator_label.setObjectName("cameraStatus")
        top_row.addWidget(operator_label)
        top_row.addStretch(1)
        top_row.addWidget(QLabel("作業相機"))
        self.camera_combo = QComboBox()
        self.camera_combo.setMinimumWidth(260)
        self.camera_combo.currentIndexChanged.connect(self.persist_selected_camera)
        top_row.addWidget(self.camera_combo)
        card_layout.addLayout(top_row)

        mode_grid = QGridLayout()
        mode_grid.setContentsMargins(0, 0, 0, 0)
        mode_grid.setHorizontalSpacing(14)
        mode_grid.setVerticalSpacing(14)

        shipment_button = create_mode_button("出貨作業")
        repair_button = create_mode_button("維修收貨")
        return_button = create_mode_button("退貨收貨")
        shipment_button.clicked.connect(lambda: self.open_child_window(ShipmentWindow(self, self.selected_camera_name(), self.draft_service)))
        repair_button.clicked.connect(lambda: self.open_child_window(RepairReceivingWindow(self, self.selected_camera_name(), self.draft_service)))
        return_button.clicked.connect(lambda: self.open_child_window(ReturnReceivingWindow(self, self.selected_camera_name(), self.draft_service)))
        mode_grid.addWidget(shipment_button, 0, 0)
        mode_grid.addWidget(repair_button, 0, 1)
        mode_grid.addWidget(return_button, 1, 0, 1, 2)
        card_layout.addLayout(mode_grid)

        action_row = QHBoxLayout()
        settings_button = QPushButton("系統設定")
        settings_button.setObjectName("secondaryButton")
        settings_button.clicked.connect(self.open_settings)
        back_button = QPushButton("返回登入")
        back_button.setObjectName("secondaryButton")
        back_button.clicked.connect(self.go_back)
        action_row.addWidget(settings_button)
        action_row.addWidget(back_button)
        action_row.addStretch(1)
        card_layout.addLayout(action_row)

        container.layout.addWidget(card)
        container.layout.addStretch(1)
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
