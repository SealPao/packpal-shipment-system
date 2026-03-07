import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QLineEdit, QPushButton

from services.camera_service import CameraOption
from ui.login_window import LoginWindow
from ui.mode_select_window import ModeSelectWindow
from ui.repair_receiving_window import RepairReceivingWindow
from ui.return_receiving_window import ReturnReceivingWindow
from ui.shipment_window import ShipmentWindow


class FakeCameraService:
    def __init__(self) -> None:
        self.cameras = [
            CameraOption(id="cam-1", name="USB Camera"),
            CameraOption(id="cam-2", name="Document Camera"),
        ]
        self.selected_id = "cam-2"

    def list_cameras(self) -> list[CameraOption]:
        return self.cameras

    def load_selected_camera_id(self) -> str:
        return self.selected_id

    def save_selected_camera_id(self, camera_id: str) -> None:
        self.selected_id = camera_id

    def get_selected_camera(self, cameras: list[CameraOption] | None = None) -> CameraOption | None:
        available = cameras if cameras is not None else self.cameras
        for camera in available:
            if camera.id == self.selected_id:
                return camera
        return available[0] if available else None


app = QApplication.instance() or QApplication([])
QSettings().clear()


def test_login_window_renders_expected_shell() -> None:
    window = LoginWindow()
    labels = [label.text() for label in window.findChildren(QLabel)]

    assert window.windowTitle() == "出貨小幫手 - 登入"
    assert "請登入系統以開始作業" in labels
    assert any("Version v0.1.0" in text for text in labels)


def test_mode_selection_window_renders_all_three_modes() -> None:
    window = ModeSelectWindow(camera_service=FakeCameraService())
    buttons = [button.text() for button in window.findChildren(QPushButton)]
    combo = window.findChild(QComboBox)

    assert "出貨作業" in buttons
    assert "維修收貨" in buttons
    assert "退貨收貨" in buttons
    assert "返回登入" in buttons
    assert combo is not None
    assert combo.count() == 2
    assert combo.currentText() == "Document Camera"


def test_shipment_window_renders_contract_aligned_fields() -> None:
    window = ShipmentWindow(selected_camera_name="Document Camera")
    labels = [label.text() for label in window.findChildren(QLabel)]
    placeholders = [field.placeholderText() for field in window.findChildren(QLineEdit)]

    assert window.windowTitle() == "出貨小幫手 - 出貨作業"
    assert "Record Summary" in labels
    assert "目前選擇的相機：Document Camera" in labels
    assert any(text == "預留欄位：record_no" for text in placeholders)
    assert any(text == "預留欄位：attachments" for text in placeholders)


def test_repair_window_renders_contract_aligned_fields() -> None:
    window = RepairReceivingWindow(selected_camera_name="USB Camera")
    labels = [label.text() for label in window.findChildren(QLabel)]
    placeholders = [field.placeholderText() for field in window.findChildren(QLineEdit)]

    assert window.windowTitle() == "出貨小幫手 - 維修收貨"
    assert "Repair Details" in labels
    assert "目前選擇的相機：USB Camera" in labels
    assert any(text == "預留欄位：notes" for text in placeholders)
    assert any(text == "預留欄位：device_serial" for text in placeholders)


def test_return_window_renders_contract_aligned_fields() -> None:
    window = ReturnReceivingWindow(selected_camera_name="Document Camera")
    labels = [label.text() for label in window.findChildren(QLabel)]
    placeholders = [field.placeholderText() for field in window.findChildren(QLineEdit)]

    assert window.windowTitle() == "出貨小幫手 - 退貨收貨"
    assert "Return Details" in labels
    assert "目前選擇的相機：Document Camera" in labels
    assert any(text == "預留欄位：return_reason" for text in placeholders)
    assert any(text == "預留欄位：attachments" for text in placeholders)