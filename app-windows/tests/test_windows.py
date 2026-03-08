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
from ui.app_window import AppWindow


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


def build_window() -> AppWindow:
    settings_service = SettingsService()
    employee_service = EmployeeService(settings_service)
    return AppWindow(
        settings_service=settings_service,
        employee_service=employee_service,
        camera_service=FakeCameraService(),
        draft_service=DraftService(unique_db_path("drafts")),
    )


def test_app_window_uses_single_stack_flow() -> None:
    write_employee_file()
    window = build_window()
    edits = window.login_page.findChildren(QLineEdit)
    buttons = [button.text() for button in window.login_page.findChildren(QPushButton)]

    assert window.windowTitle() == "出貨小幫手 - 進入作業"
    assert window.stack.currentWidget() is window.login_page
    assert len(edits) == 1
    assert window.login_page.employee_id_input.placeholderText() == "請輸入您的員工號碼"
    assert "系統設定" in buttons
    assert "請點我開始工作" in buttons

    window.login_page.employee_id_input.setText("342")
    assert "歡迎尊貴的 342 包兆強" in window.login_page.enter_button.text()

    window.login_page.handle_enter()
    assert window.stack.currentWidget() is window.mode_page
    assert window.isMaximized() is False


def test_settings_page_renders_employee_actions() -> None:
    write_employee_file()
    window = build_window()
    window.show_settings("login")
    labels = [label.text() for label in window.settings_page.findChildren(QLabel)]
    table = window.settings_page.findChild(QTableWidget)
    buttons = [button.text() for button in window.settings_page.findChildren(QPushButton)]

    assert "NAS API 位址" in labels
    assert "員工資料設定" in labels
    assert "新增一筆" in buttons
    assert "刪除選取" in buttons
    assert "儲存員工資料" in buttons
    assert table is not None
    assert table.columnCount() == 2


def test_mode_selection_page_renders_simple_actions() -> None:
    write_employee_file()
    window = build_window()
    window.show_mode(EmployeeRecord(employee_id="342", name="包兆強"))
    buttons = [button.text() for button in window.mode_page.findChildren(QPushButton)]
    combo = window.mode_page.findChild(QComboBox)
    labels = [label.text() for label in window.mode_page.findChildren(QLabel)]

    assert "出貨作業" in buttons
    assert "維修收貨" in buttons
    assert "退貨收貨" in buttons
    assert "系統設定" in buttons
    assert combo is not None
    assert combo.currentText() == "Document Camera"
    assert "目前操作人員：342 / 包兆強" in labels
    assert "選擇作業模式" in labels


def test_shipment_page_can_save_and_load_draft() -> None:
    write_employee_file()
    window = build_window()
    window.show_mode(EmployeeRecord(employee_id="342", name="包兆強"))
    window.show_workflow("shipment")
    labels = [label.text() for label in window.shipment_page.findChildren(QLabel)]

    window.shipment_page.scan_input.setText("SHP-TEST-001")
    window.shipment_page.save_draft()
    window.shipment_page.load_latest_draft()

    back_button = next(button for button in window.shipment_page.findChildren(QPushButton) if button.text() == "返回模式選擇")
    back_button.click()

    assert any("請掃描單號開始錄影" in text for text in labels)
    assert window.shipment_page.scan_input.text() == "SHP-TEST-001"
    assert window.stack.currentWidget() is window.mode_page


def test_repair_and_return_pages_render_stage_ui() -> None:
    write_employee_file()
    window = build_window()
    window.show_mode(EmployeeRecord(employee_id="342", name="包兆強"))

    window.show_workflow("repair")
    repair_labels = [label.text() for label in window.repair_page.findChildren(QLabel)]
    assert "維修收貨" in repair_labels
    assert "請掃描維修單號開始收貨" in repair_labels

    window.show_workflow("return")
    return_labels = [label.text() for label in window.return_page.findChildren(QLabel)]
    assert "退貨收貨" in return_labels
    assert "請掃描退貨單號開始收貨" in return_labels


def test_database_initialization_creates_record_drafts_table() -> None:
    db_path = unique_db_path("db")
    initialize_database(db_path)
    with connect(db_path) as connection:
        row = connection.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'record_drafts'").fetchone()
    assert row is not None

