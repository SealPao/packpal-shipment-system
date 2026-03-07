from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QMainWindow, QPushButton, QWidget

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from services.camera_service import CameraOption, CameraService
from ui.common import ScreenContainer, app_stylesheet, build_footer, create_card, create_mode_button, create_page_header
from ui.repair_receiving_window import RepairReceivingWindow
from ui.return_receiving_window import ReturnReceivingWindow
from ui.shipment_window import ShipmentWindow


class ModeSelectWindow(QMainWindow):
    def __init__(self, parent_login: QMainWindow | None = None, camera_service: CameraService | None = None) -> None:
        super().__init__(parent_login)
        self.parent_login = parent_login
        self.child_window: QMainWindow | None = None
        self.camera_service = camera_service or CameraService()
        self.cameras: list[CameraOption] = []

        self.setWindowTitle(f"{APP_TITLE} - 模式選擇")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        container = ScreenContainer()
        self.setCentralWidget(container)

        card, card_layout = create_card()
        card_layout.addWidget(self._build_camera_section())

        shipment_button = create_mode_button("出貨作業")
        repair_button = create_mode_button("維修收貨")
        return_button = create_mode_button("退貨收貨")
        back_button = QPushButton("返回登入")
        back_button.setObjectName("secondaryButton")
        back_button.setMinimumHeight(42)

        shipment_button.clicked.connect(lambda: self.open_child_window(ShipmentWindow(self, self.selected_camera_name())))
        repair_button.clicked.connect(lambda: self.open_child_window(RepairReceivingWindow(self, self.selected_camera_name())))
        return_button.clicked.connect(lambda: self.open_child_window(ReturnReceivingWindow(self, self.selected_camera_name())))
        back_button.clicked.connect(self.go_back)

        card_layout.addWidget(shipment_button)
        card_layout.addWidget(repair_button)
        card_layout.addWidget(return_button)
        card_layout.addSpacing(8)
        card_layout.addWidget(back_button)

        container.layout.addStretch(1)
        container.layout.addWidget(
            create_page_header(
                "請選擇作業模式",
                "進入作業前可先指定要使用的相機，避免後續流程直接占用到錯的 webcam。",
            )
        )
        container.layout.addWidget(card)
        container.layout.addStretch(1)
        container.layout.addWidget(build_footer())

        self.refresh_camera_options()
        self.setStyleSheet(app_stylesheet("#0f766e", "#0d5f59"))

    def _build_camera_section(self) -> QWidget:
        wrapper = QWidget()
        layout = QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        label = QLabel("相機裝置")
        label.setMinimumWidth(90)

        self.camera_combo = QComboBox()
        self.camera_combo.currentIndexChanged.connect(self.persist_selected_camera)

        self.refresh_button = QPushButton("重新整理相機")
        self.refresh_button.setObjectName("secondaryButton")
        self.refresh_button.clicked.connect(self.refresh_camera_options)

        self.camera_status_label = QLabel()
        self.camera_status_label.setObjectName("cameraStatus")

        layout.addWidget(label)
        layout.addWidget(self.camera_combo, 1)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.camera_status_label)
        return wrapper

    def refresh_camera_options(self) -> None:
        self.cameras = self.camera_service.list_cameras()
        selected_camera = self.camera_service.get_selected_camera(self.cameras)

        self.camera_combo.blockSignals(True)
        self.camera_combo.clear()

        if not self.cameras:
            self.camera_combo.addItem("未偵測到相機", "")
            self.camera_combo.setEnabled(False)
            self.camera_status_label.setText("目前沒有可用相機")
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
                self.camera_status_label.setText(f"已選擇：{selected_camera.name}")
            else:
                self.camera_status_label.setText("請選擇相機")

            self.camera_combo.setCurrentIndex(selected_index)

        self.camera_combo.blockSignals(False)

    def persist_selected_camera(self) -> None:
        camera_id = str(self.camera_combo.currentData())
        if not camera_id:
            return

        self.camera_service.save_selected_camera_id(camera_id)
        self.camera_status_label.setText(f"已選擇：{self.selected_camera_name()}")

    def selected_camera_name(self) -> str | None:
        camera_id = str(self.camera_combo.currentData())
        for camera in self.cameras:
            if camera.id == camera_id:
                return camera.name
        return None

    def open_child_window(self, window: QMainWindow) -> None:
        self.child_window = window
        self.child_window.show()
        self.hide()

    def go_back(self) -> None:
        if self.parent_login is not None:
            self.parent_login.show()
        self.close()