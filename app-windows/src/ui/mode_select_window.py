from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from ui.common import ScreenContainer, build_footer, create_mode_button


class ModeSelectWindow(QMainWindow):
    def __init__(self, parent_login: QMainWindow | None = None) -> None:
        super().__init__(parent_login)
        self.parent_login = parent_login

        self.setWindowTitle(f"{APP_TITLE} - 模式選擇")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        container = ScreenContainer()
        self.setCentralWidget(container)

        title = QLabel("請選擇作業模式")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("目前僅提供流程骨架，後續再接入實際業務流程。")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        shipment_button = create_mode_button("出貨作業")
        repair_button = create_mode_button("維修收貨")
        return_button = create_mode_button("退貨收貨")
        back_button = QPushButton("返回登入")
        back_button.setMinimumHeight(42)

        shipment_button.clicked.connect(lambda: self.show_placeholder("出貨作業"))
        repair_button.clicked.connect(lambda: self.show_placeholder("維修收貨"))
        return_button.clicked.connect(lambda: self.show_placeholder("退貨收貨"))
        back_button.clicked.connect(self.go_back)

        card_layout.addWidget(shipment_button)
        card_layout.addWidget(repair_button)
        card_layout.addWidget(return_button)
        card_layout.addSpacing(8)
        card_layout.addWidget(back_button)

        container.layout.addStretch(1)
        container.layout.addWidget(title)
        container.layout.addWidget(subtitle)
        container.layout.addWidget(card)
        container.layout.addStretch(1)
        container.layout.addWidget(build_footer())

        self.setStyleSheet(_build_stylesheet())

    def show_placeholder(self, mode_name: str) -> None:
        QMessageBox.information(self, "尚未實作", f"{mode_name} 模組將於後續版本接入。")

    def go_back(self) -> None:
        if self.parent_login is not None:
            self.parent_login.show()
        self.close()



def _build_stylesheet() -> str:
    return """
        QMainWindow {
            background-color: #f5f7fb;
        }
        #screenContainer {
            background-color: #f5f7fb;
        }
        #pageTitle {
            font-size: 28px;
            font-weight: 700;
            color: #1f2937;
        }
        #pageSubtitle {
            font-size: 15px;
            color: #4b5563;
        }
        #card {
            background-color: white;
            border: 1px solid #dbe2ea;
            border-radius: 16px;
        }
        QPushButton {
            padding: 10px 18px;
            border: none;
            border-radius: 10px;
            background-color: #0f766e;
            color: white;
            font-size: 15px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: #0d5f59;
        }
        #footerLabel {
            font-size: 12px;
            color: #6b7280;
        }
    """
