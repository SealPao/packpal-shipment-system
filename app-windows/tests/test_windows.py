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


def test_shipment_window_renders_expected_sections() -> None:
    window = ShipmentWindow()
    labels = [label.text() for label in window.findChildren(QLabel)]
    placeholders = [field.placeholderText() for field in window.findChildren(QLineEdit)]

    assert window.windowTitle() == "出貨小幫手 - 出貨作業"
    assert "預計整合的出貨步驟" in labels
    assert "基本資料" in labels
    assert any("預留欄位：出貨單號" == text for text in placeholders)


def test_repair_window_renders_expected_sections() -> None:
    window = RepairReceivingWindow()
    labels = [label.text() for label in window.findChildren(QLabel)]
    placeholders = [field.placeholderText() for field in window.findChildren(QLineEdit)]

    assert window.windowTitle() == "出貨小幫手 - 維修收貨"
    assert "預計整合的維修收貨步驟" in labels
    assert "收件資料" in labels
    assert any("預留欄位：故障描述" == text for text in placeholders)


def test_return_window_renders_expected_sections() -> None:
    window = ReturnReceivingWindow()
    labels = [label.text() for label in window.findChildren(QLabel)]
    placeholders = [field.placeholderText() for field in window.findChildren(QLineEdit)]

    assert window.windowTitle() == "出貨小幫手 - 退貨收貨"
    assert "預計整合的退貨收貨步驟" in labels
    assert "退貨資料" in labels
    assert any("預留欄位：退貨原因" == text for text in placeholders)