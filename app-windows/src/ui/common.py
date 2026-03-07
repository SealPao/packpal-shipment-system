from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from app.version import APP_VERSION


FOOTER_TEXT = (
    "Copyright © 默默工作的小包\n"
    "有任何問題，請聯繫小包來獲得更多支援，歡迎打賞餵食。\n"
    f"Version v{APP_VERSION}"
)


def build_footer() -> QLabel:
    footer = QLabel(FOOTER_TEXT)
    footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
    footer.setObjectName("footerLabel")
    footer.setWordWrap(True)
    return footer


def create_mode_button(label: str) -> QPushButton:
    button = QPushButton(label)
    button.setMinimumHeight(68)
    button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    return button


class ScreenContainer(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("screenContainer")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(32, 32, 32, 24)
        self.layout.setSpacing(20)
