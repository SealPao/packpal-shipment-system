from __future__ import annotations

from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from app.config import logo_path
from app.version import APP_VERSION


FOOTER_TEXT = (
    "Copyright © 默默工作的小包\n"
    "有任何問題，請聯繫小包來獲得更多支援，歡迎打賞餵食。\n"
    f"Version v{APP_VERSION}"
)


def apply_window_icon(window: QWidget) -> None:
    path = logo_path()
    if path.exists():
        window.setWindowIcon(QIcon(str(path)))


def show_window_like(source: QWidget, target: QWidget) -> None:
    if source.isFullScreen():
        target.showFullScreen()
        return
    if source.isMaximized():
        target.showMaximized()
        return
    target.showNormal()
    target.move(source.pos())
    target.resize(source.size())
    target.show()


def build_footer() -> QLabel:
    footer = QLabel(FOOTER_TEXT)
    footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
    footer.setObjectName("footerLabel")
    footer.setWordWrap(True)
    return footer


def _trim_transparent_edges(pixmap: QPixmap) -> QPixmap:
    image = pixmap.toImage().convertToFormat(pixmap.toImage().format())
    if not image.hasAlphaChannel():
        return pixmap

    left = image.width()
    top = image.height()
    right = -1
    bottom = -1

    for y in range(image.height()):
        for x in range(image.width()):
            if image.pixelColor(x, y).alpha() > 0:
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    if right < left or bottom < top:
        return pixmap

    rect = QRect(left, top, right - left + 1, bottom - top + 1)
    return pixmap.copy(rect)


def set_logo_height(logo: QLabel, max_height: int) -> None:
    logo.setMinimumHeight(max_height)
    logo.setMaximumHeight(max_height)
    path = logo_path()
    if path.exists():
        pixmap = _trim_transparent_edges(QPixmap(str(path)))
        scaled = pixmap.scaled(
            int(max_height * 2.4),
            max_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        logo.setPixmap(scaled)


def build_logo_label(max_height: int = 140) -> QLabel:
    logo = QLabel()
    logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
    logo.setObjectName("logoLabel")
    set_logo_height(logo, max_height)
    return logo


def create_mode_button(label: str) -> QPushButton:
    button = QPushButton(label)
    button.setObjectName("modeButton")
    button.setMinimumHeight(180)
    button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    return button


class ScreenContainer(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("screenContainer")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(32, 24, 32, 24)
        self.layout.setSpacing(20)


def create_page_header(title_text: str, subtitle_text: str, *, show_logo: bool = True) -> QWidget:
    header = QWidget()
    layout = QVBoxLayout(header)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(10)

    if show_logo:
        layout.addWidget(build_logo_label())

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


def create_split_header(title_text: str, subtitle_text: str) -> QWidget:
    header = QWidget()
    layout = QHBoxLayout(header)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(24)

    logo = build_logo_label(128)
    logo.setMinimumWidth(220)
    layout.addWidget(logo, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

    text_wrap = QWidget()
    text_layout = QVBoxLayout(text_wrap)
    text_layout.setContentsMargins(0, 0, 0, 0)
    text_layout.setSpacing(10)

    title = QLabel(title_text)
    title.setObjectName("heroTitle")

    subtitle = QLabel(subtitle_text)
    subtitle.setObjectName("heroSubtitle")
    subtitle.setWordWrap(True)

    text_layout.addStretch(1)
    text_layout.addWidget(title)
    text_layout.addWidget(subtitle)
    text_layout.addStretch(1)

    layout.addWidget(text_wrap, 1)
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
        #heroTitle {{ font-size: 36px; font-weight: 800; color: #0f172a; }}
        #heroSubtitle {{ font-size: 20px; color: #475569; }}
        #sectionTitle {{ font-size: 18px; font-weight: 700; color: #1f2937; }}
        #sectionBody {{ font-size: 14px; color: #4b5563; line-height: 1.6; }}
        #subSectionTitle {{ font-size: 15px; font-weight: 700; color: #111827; }}
        #fieldLabel {{ font-size: 13px; color: #94a3b8; }}
        #heroName {{ font-size: 22px; font-weight: 700; color: #0f172a; }}
        #cameraStatus, #draftStatus, #settingsHint, #employeeStatus {{ font-size: 13px; color: #334155; }}
        #card {{ background-color: white; border: 1px solid #dbe2ea; border-radius: 16px; }}
        #subCard {{ background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; }}
        #heroInputShell {{ background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; }}
        #heroInputHint {{ font-size: 12px; color: #94a3b8; padding-left: 4px; }}
        QLabel {{ color: #111827; }}
        QLineEdit, QComboBox {{ min-height: 38px; padding: 6px 10px; border: 1px solid #cbd5e1; border-radius: 8px; background-color: #ffffff; }}
        QLineEdit::placeholder {{ color: #94a3b8; }}
        #heroInput {{ min-height: 56px; font-size: 30px; padding: 4px 12px; color: #111827; border: none; background: transparent; }}
        QTableWidget {{ border: 1px solid #cbd5e1; border-radius: 10px; background-color: white; gridline-color: #e5e7eb; }}
        QHeaderView::section {{ background-color: #f8fafc; color: #0f172a; padding: 10px; border: none; border-bottom: 1px solid #e5e7eb; font-weight: 700; }}
        QPushButton {{ padding: 10px 18px; border: none; border-radius: 10px; background-color: {primary_color}; color: white; font-size: 15px; font-weight: 600; }}
        QPushButton:hover {{ background-color: {hover_color}; }}
        #secondaryButton {{ background-color: #e5e7eb; color: #111827; }}
        #secondaryButton:hover {{ background-color: #d1d5db; }}
        #modeButton {{ text-align: center; padding: 18px 20px; background-color: white; color: #0f172a; border: 1px solid #cbd5e1; font-size: 30px; font-weight: 800; border-radius: 18px; }}
        #modeButton:hover {{ background-color: #ecfeff; border: 1px solid #14b8a6; color: #0f172a; }}
        #footerLabel {{ font-size: 12px; color: #6b7280; }}
    """







