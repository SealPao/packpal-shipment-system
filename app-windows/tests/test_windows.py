import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton

from ui.login_window import LoginWindow
from ui.mode_select_window import ModeSelectWindow
from ui.repair_receiving_window import RepairReceivingWindow
from ui.return_receiving_window import ReturnReceivingWindow
from ui.shipment_window import ShipmentWindow


app = QApplication.instance() or QApplication([])


def test_login_window_renders_expected_shell() -> None:
    window = LoginWindow()
    labels = [label.text() for label in window.findChildren(QLabel)]

    assert window.windowTitle() == "出貨小幫手 - 登入"
    assert "請登入系統以開始作業" in labels
    assert any("Version v0.1.0" in text for text in labels)


def test_mode_selection_window_renders_all_three_modes() -> None:
    window = ModeSelectWindow()
    buttons = [button.text() for button in window.findChildren(QPushButton)]

    assert "出貨作業" in buttons
    assert "維修收貨" in buttons
    assert "退貨收貨" in buttons
    assert "返回登入" in buttons


def test_shipment_window_renders_contract_aligned_fields() -> None:
    window = ShipmentWindow()
    labels = [label.text() for label in window.findChildren(QLabel)]
    placeholders = [field.placeholderText() for field in window.findChildren(QLineEdit)]

    assert window.windowTitle() == "出貨小幫手 - 出貨作業"
    assert "Record Summary" in labels
    assert any(text == "預留欄位：record_no" for text in placeholders)
    assert any(text == "預留欄位：attachments" for text in placeholders)


def test_repair_window_renders_contract_aligned_fields() -> None:
    window = RepairReceivingWindow()
    labels = [label.text() for label in window.findChildren(QLabel)]
    placeholders = [field.placeholderText() for field in window.findChildren(QLineEdit)]

    assert window.windowTitle() == "出貨小幫手 - 維修收貨"
    assert "Repair Details" in labels
    assert any(text == "預留欄位：notes" for text in placeholders)
    assert any(text == "預留欄位：device_serial" for text in placeholders)


def test_return_window_renders_contract_aligned_fields() -> None:
    window = ReturnReceivingWindow()
    labels = [label.text() for label in window.findChildren(QLabel)]
    placeholders = [field.placeholderText() for field in window.findChildren(QLineEdit)]

    assert window.windowTitle() == "出貨小幫手 - 退貨收貨"
    assert "Return Details" in labels
    assert any(text == "預留欄位：return_reason" for text in placeholders)
    assert any(text == "預留欄位：attachments" for text in placeholders)