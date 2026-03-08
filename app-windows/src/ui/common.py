from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

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


def create_page_header(title_text: str, subtitle_text: str) -> QWidget:
    header = QWidget()
    layout = QVBoxLayout(header)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)

    title = QLabel(title_text)
    title.setObjectName("pageTitle")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)

    subtitle = QLabel(subtitle_text)
    subtitle.setObjectName("pageSubtitle")
    subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
    subtitle.setWordWrap(True)

    layout.addWidget(title)
    layout.addWidget(subtitle)
    return header


def create_card() -> tuple[QFrame, QVBoxLayout]:
    card = QFrame()
    card.setObjectName("card")
    layout = QVBoxLayout(card)
    layout.setContentsMargins(24, 24, 24, 24)
    layout.setSpacing(16)
    return card, layout


def create_back_row(button_text: str = "返回模式選擇") -> tuple[QWidget, QPushButton]:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(12)

    back_button = QPushButton(button_text)
    back_button.setObjectName("secondaryButton")
    back_button.setMinimumHeight(42)

    layout.addWidget(back_button)
    layout.addStretch(1)
    return row, back_button


def app_stylesheet(primary_color: str = "#2563eb", hover_color: str = "#1d4ed8") -> str:
    return f"""
        QMainWindow {{ background-color: #f5f7fb; }}
        #screenContainer {{ background-color: #f5f7fb; }}
        #pageTitle {{ font-size: 28px; font-weight: 700; color: #1f2937; }}
        #pageSubtitle {{ font-size: 15px; color: #4b5563; }}
        #sectionTitle {{ font-size: 18px; font-weight: 700; color: #1f2937; }}
        #sectionBody {{ font-size: 14px; color: #4b5563; line-height: 1.6; }}
        #subSectionTitle {{ font-size: 15px; font-weight: 700; color: #111827; }}
        #fieldLabel {{ font-size: 13px; color: #374151; }}
        #cameraStatus, #draftStatus, #settingsHint {{ font-size: 13px; color: #334155; }}
        #card {{ background-color: white; border: 1px solid #dbe2ea; border-radius: 16px; }}
        #subCard {{ background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; }}
        QLabel {{ color: #111827; }}
        QLineEdit, QComboBox {{ min-height: 38px; padding: 6px 10px; border: 1px solid #cbd5e1; border-radius: 8px; background-color: #ffffff; }}
        QPushButton {{ padding: 10px 18px; border: none; border-radius: 10px; background-color: {primary_color}; color: white; font-size: 15px; font-weight: 600; }}
        QPushButton:hover {{ background-color: {hover_color}; }}
        #secondaryButton {{ background-color: #e5e7eb; color: #111827; }}
        #secondaryButton:hover {{ background-color: #d1d5db; }}
        #footerLabel {{ font-size: 12px; color: #6b7280; }}
    """