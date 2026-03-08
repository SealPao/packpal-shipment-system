import csv
import os
from pathlib import Path
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QLineEdit, QPushButton, QTableWidget

from db.session import connect, initialize_database
from services.camera_service import CameraOption
from services.draft_service import DraftService
from services.employee_service import EmployeeRecord, EmployeeService
from services.settings_service import SettingsService
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


def write_employee_file() -> None:
    service = EmployeeService(SettingsService())
    target = service.employee_file_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["employee_id", "name"])
        writer.writeheader()
        writer.writerow({"employee_id": "342", "name": "包兆強"})
        writer.writerow({"employee_id": "A002", "name": "陳美玲"})


def test_login_window_uses_employee_lookup() -> None:
    write_employee_file()
    window = LoginWindow()
    edits = window.findChildren(QLineEdit)
    buttons = [button.text() for button in window.findChildren(QPushButton)]

    assert window.windowTitle() == "出貨小幫手 - 進入作業"
    assert len(edits) == 1
    assert edits[0].placeholderText() == "員工號碼"
    assert "系統設定" in buttons
    assert "請點我開始工作" in buttons

    window.employee_id_input.setText("342")
    assert window.employee_name_label.text() == "歡迎尊貴的 342 包兆強"
    assert "歡迎尊貴的 342 包兆強" in window.enter_button.text()


def test_settings_window_renders_employee_actions() -> None:
    write_employee_file()
    window = SettingsWindow()
    labels = [label.text() for label in window.findChildren(QLabel)]
    table = window.findChild(QTableWidget)
    buttons = [button.text() for button in window.findChildren(QPushButton)]

    assert "NAS API 位址" in labels
    assert "員工資料設定" in labels
    assert "新增一筆" in buttons
    assert "刪除選取" in buttons
    assert "儲存員工資料" in buttons
    assert table is not None
    assert table.columnCount() == 2


def test_mode_selection_window_renders_simple_actions() -> None:
    employee = EmployeeRecord(employee_id="342", name="包兆強")
    window = ModeSelectWindow(current_employee=employee, camera_service=FakeCameraService(), draft_service=DraftService(unique_db_path("mode")))
    buttons = [button.text() for button in window.findChildren(QPushButton)]
    combo = window.findChild(QComboBox)
    labels = [label.text() for label in window.findChildren(QLabel)]

    assert "出貨作業" in buttons
    assert "維修收貨" in buttons
    assert "退貨收貨" in buttons
    assert "系統設定" in buttons
    assert combo is not None
    assert combo.currentText() == "Document Camera"
    assert "目前操作人員：342 / 包兆強" in labels


def test_shipment_window_can_save_and_load_draft() -> None:
    draft_service = DraftService(unique_db_path("shipment"))
    window = ShipmentWindow(selected_camera_name="Document Camera", draft_service=draft_service)
    labels = [label.text() for label in window.findChildren(QLabel)]

    window.scan_input.setText("SHP-TEST-001")
    window.save_draft()

    reloaded = ShipmentWindow(selected_camera_name="Document Camera", draft_service=draft_service)
    reloaded.load_latest_draft()

    assert any("請掃描單號開始錄影" in text for text in labels)
    assert reloaded.scan_input.text() == "SHP-TEST-001"


def test_repair_window_renders_contract_aligned_fields() -> None:
    window = RepairReceivingWindow(selected_camera_name="USB Camera", draft_service=DraftService(unique_db_path("repair")))
    labels = [label.text() for label in window.findChildren(QLabel)]
    placeholders = [field.placeholderText() for field in window.findChildren(QLineEdit)]

    assert window.windowTitle() == "出貨小幫手 - 維修收貨"
    assert "維修資訊" in labels
    assert "目前相機：USB Camera" in labels
    assert any(text == "請輸入 備註" for text in placeholders)


def test_return_window_renders_contract_aligned_fields() -> None:
    window = ReturnReceivingWindow(selected_camera_name="Document Camera", draft_service=DraftService(unique_db_path("return")))
    labels = [label.text() for label in window.findChildren(QLabel)]
    placeholders = [field.placeholderText() for field in window.findChildren(QLineEdit)]

    assert window.windowTitle() == "出貨小幫手 - 退貨收貨"
    assert "退貨資訊" in labels
    assert any(text == "請輸入 退貨原因" for text in placeholders)


def test_database_initialization_creates_record_drafts_table() -> None:
    db_path = unique_db_path("db")
    initialize_database(db_path)
    with connect(db_path) as connection:
        row = connection.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'record_drafts'").fetchone()
    assert row is not None


