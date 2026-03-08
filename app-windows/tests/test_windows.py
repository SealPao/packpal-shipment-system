import os
from pathlib import Path
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QLineEdit, QPushButton

from db.session import connect, initialize_database
from services.camera_service import CameraOption
from services.draft_service import DraftService
from ui.login_window import LoginWindow
from ui.mode_select_window import ModeSelectWindow
from ui.repair_receiving_window import RepairReceivingWindow
from ui.return_receiving_window import ReturnReceivingWindow
from ui.settings_window import SettingsWindow
from ui.shipment_window import ShipmentWindow


class FakeCameraService:
    def __init__(self) -> None:
        self.cameras = [
            CameraOption(id="cam-1", name="USB Camera"),
            CameraOption(id="cam-2", name="Document Camera"),
        ]
        self.selected_id = "cam-2"

    def list_cameras(self):
        return self.cameras

    def load_selected_camera_id(self):
        return self.selected_id

    def save_selected_camera_id(self, camera_id: str):
        self.selected_id = camera_id

    def get_selected_camera(self, cameras=None):
        available = cameras if cameras is not None else self.cameras
        for camera in available:
            if camera.id == self.selected_id:
                return camera
        return available[0] if available else None


app = QApplication.instance() or QApplication([])
QSettings().clear()


def unique_db_path(name: str) -> Path:
    return Path(tempfile.gettempdir()) / f"{name}-{os.getpid()}.db"


def test_login_window_uses_operator_name_only() -> None:
    window = LoginWindow()
    labels = [label.text() for label in window.findChildren(QLabel)]
    edits = window.findChildren(QLineEdit)
    buttons = [button.text() for button in window.findChildren(QPushButton)]

    assert window.windowTitle() == "出貨小幫手 - 進入作業"
    assert "輸入操作人員名稱後即可開始，不需要密碼。" in labels
    assert len(edits) == 1
    assert edits[0].placeholderText() == "請輸入操作人員名稱"
    assert "系統設定" in buttons
    assert "進入作業" in buttons


def test_settings_window_renders_core_fields() -> None:
    window = SettingsWindow()
    labels = [label.text() for label in window.findChildren(QLabel)]

    assert "預設操作人員" in labels
    assert "NAS API 位址" in labels
    assert "本地儲存路徑" in labels


def test_mode_selection_window_renders_camera_and_settings() -> None:
    window = ModeSelectWindow(camera_service=FakeCameraService(), draft_service=DraftService(unique_db_path('mode')))
    buttons = [button.text() for button in window.findChildren(QPushButton)]
    combo = window.findChild(QComboBox)

    assert "出貨作業" in buttons
    assert "維修收貨" in buttons
    assert "退貨收貨" in buttons
    assert "系統設定" in buttons
    assert combo is not None
    assert combo.count() == 2
    assert combo.currentText() == "Document Camera"


def test_shipment_window_can_save_and_load_draft() -> None:
    draft_service = DraftService(unique_db_path('shipment'))
    window = ShipmentWindow(selected_camera_name="Document Camera", draft_service=draft_service)
    labels = [label.text() for label in window.findChildren(QLabel)]

    window.fields["record_no"].setText("SHP-TEST-001")
    window.fields["notes"].setText("Draft note")
    window.save_draft()

    reloaded = ShipmentWindow(selected_camera_name="Document Camera", draft_service=draft_service)
    reloaded.load_latest_draft(show_empty_message=True)

    assert "目前選擇的相機：Document Camera" in labels
    assert reloaded.fields["record_no"].text() == "SHP-TEST-001"
    assert reloaded.fields["notes"].text() == "Draft note"


def test_repair_window_renders_contract_aligned_fields() -> None:
    window = RepairReceivingWindow(selected_camera_name="USB Camera", draft_service=DraftService(unique_db_path('repair')))
    labels = [label.text() for label in window.findChildren(QLabel)]
    placeholders = [field.placeholderText() for field in window.findChildren(QLineEdit)]

    assert window.windowTitle() == "出貨小幫手 - 維修收貨"
    assert "Repair Details" in labels
    assert "目前選擇的相機：USB Camera" in labels
    assert any(text == "預留欄位：notes" for text in placeholders)


def test_return_window_renders_contract_aligned_fields() -> None:
    window = ReturnReceivingWindow(selected_camera_name="Document Camera", draft_service=DraftService(unique_db_path('return')))
    labels = [label.text() for label in window.findChildren(QLabel)]
    placeholders = [field.placeholderText() for field in window.findChildren(QLineEdit)]

    assert window.windowTitle() == "出貨小幫手 - 退貨收貨"
    assert "Return Details" in labels
    assert any(text == "預留欄位：return_reason" for text in placeholders)


def test_database_initialization_creates_record_drafts_table() -> None:
    db_path = unique_db_path('db')
    initialize_database(db_path)
    with connect(db_path) as connection:
        row = connection.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'record_drafts'").fetchone()
    assert row is not None