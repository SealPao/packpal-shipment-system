from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from ui.common import ScreenContainer, app_stylesheet, build_footer, create_card, create_mode_button, create_page_header
from ui.repair_receiving_window import RepairReceivingWindow
from ui.return_receiving_window import ReturnReceivingWindow
from ui.shipment_window import ShipmentWindow


class ModeSelectWindow(QMainWindow):
    def __init__(self, parent_login: QMainWindow | None = None) -> None:
        super().__init__(parent_login)
        self.parent_login = parent_login
        self.child_window: QMainWindow | None = None

        self.setWindowTitle(f"{APP_TITLE} - 模式選擇")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        container = ScreenContainer()
        self.setCentralWidget(container)

        card, card_layout = create_card()

        shipment_button = create_mode_button("出貨作業")
        repair_button = create_mode_button("維修收貨")
        return_button = create_mode_button("退貨收貨")
        back_button = QPushButton("返回登入")
        back_button.setObjectName("secondaryButton")
        back_button.setMinimumHeight(42)

        shipment_button.clicked.connect(lambda: self.open_child_window(ShipmentWindow(self)))
        repair_button.clicked.connect(lambda: self.open_child_window(RepairReceivingWindow(self)))
        return_button.clicked.connect(lambda: self.open_child_window(ReturnReceivingWindow(self)))
        back_button.clicked.connect(self.go_back)

        card_layout.addWidget(shipment_button)
        card_layout.addWidget(repair_button)
        card_layout.addWidget(return_button)
        card_layout.addSpacing(8)
        card_layout.addWidget(back_button)

        container.layout.addStretch(1)
        container.layout.addWidget(create_page_header("請選擇作業模式", "目前已建立各模式的獨立畫面骨架，後續可在各自頁面向下擴充。"))
        container.layout.addWidget(card)
        container.layout.addStretch(1)
        container.layout.addWidget(build_footer())

        self.setStyleSheet(app_stylesheet("#0f766e", "#0d5f59"))

    def open_child_window(self, window: QMainWindow) -> None:
        self.child_window = window
        self.child_window.show()
        self.hide()

    def go_back(self) -> None:
        if self.parent_login is not None:
            self.parent_login.show()
        self.close()