import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QLabel, QPushButton

from ui.login_window import LoginWindow
from ui.mode_select_window import ModeSelectWindow


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