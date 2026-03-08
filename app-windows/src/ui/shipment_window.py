from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from services.draft_service import DraftService
from ui.common import ScreenContainer, app_stylesheet, apply_window_icon, build_footer, create_back_row, create_card, create_page_header


class ShipmentWindow(QMainWindow):
    def __init__(self, parent_mode_select=None, selected_camera_name: str | None = None, draft_service: DraftService | None = None) -> None:
        super().__init__(parent_mode_select)
        self.parent_mode_select = parent_mode_select
        self.selected_camera_name = selected_camera_name or "尚未選擇"
        self.draft_service = draft_service or DraftService()

        self.setWindowTitle(f"{APP_TITLE} - 出貨作業")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        apply_window_icon(self)

        container = ScreenContainer()
        self.setCentralWidget(container)

        container.layout.addWidget(create_page_header("出貨作業", "理想流程會是先看到攝影機畫面，再掃描單號開始錄影；目前先提供骨架版介面。", show_logo=False))

        card, card_layout = create_card()
        camera_frame = QFrame()
        camera_frame.setObjectName("subCard")
        camera_layout = QVBoxLayout(camera_frame)
        camera_layout.setContentsMargins(18, 18, 18, 18)
        camera_layout.setSpacing(10)

        camera_title = QLabel(f"目前相機：{self.selected_camera_name}")
        camera_title.setObjectName("sectionTitle")
        camera_layout.addWidget(camera_title)

        preview = QLabel("攝影機畫面預留區\n\n正式版會在這裡顯示即時畫面與錄影狀態。")
        preview.setObjectName("sectionBody")
        preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview.setMinimumHeight(220)
        preview.setStyleSheet("border: 2px dashed #94a3b8; border-radius: 12px; background: #f8fafc;")
        camera_layout.addWidget(preview)

        scan_label = QLabel("請掃描單號開始錄影")
        scan_label.setObjectName("fieldLabel")
        self.scan_input = QLineEdit()
        self.scan_input.setPlaceholderText("請掃描或輸入單號")
        camera_layout.addWidget(scan_label)
        camera_layout.addWidget(self.scan_input)

        status_label = QLabel("目前尚未接入真實錄影與相機串流；此頁先做操作位置與草稿流程。")
        status_label.setObjectName("settingsHint")
        status_label.setWordWrap(True)
        camera_layout.addWidget(status_label)

        action_row = QHBoxLayout()
        save_button = QPushButton("儲存草稿")
        save_button.clicked.connect(self.save_draft)
        load_button = QPushButton("載入最近草稿")
        load_button.setObjectName("secondaryButton")
        load_button.clicked.connect(self.load_latest_draft)
        self.draft_status_label = QLabel("尚未儲存草稿")
        self.draft_status_label.setObjectName("draftStatus")
        action_row.addWidget(save_button)
        action_row.addWidget(load_button)
        action_row.addWidget(self.draft_status_label, 1)
        camera_layout.addLayout(action_row)

        card_layout.addWidget(camera_frame)
        back_row, back_button = create_back_row()
        back_button.clicked.connect(self.go_back)
        card_layout.addWidget(back_row)

        container.layout.addWidget(card)
        container.layout.addStretch(1)
        container.layout.addWidget(build_footer())

        self.load_latest_draft()
        self.setStyleSheet(app_stylesheet("#0f766e", "#0d5f59"))

    def closeEvent(self, event: QCloseEvent) -> None:
        app = QApplication.instance()
        if app is not None:
            app.quit()
        event.accept()

    def save_draft(self) -> None:
        draft_id = self.draft_service.save_draft(
            module_key="shipments",
            payload={"record_no": self.scan_input.text().strip()},
            camera_name=self.selected_camera_name,
        )
        self.draft_status_label.setText(f"草稿已儲存，編號 #{draft_id}")

    def load_latest_draft(self) -> None:
        draft = self.draft_service.latest_draft("shipments")
        payload = self.draft_service.parse_payload(draft)
        self.scan_input.setText(payload.get("record_no", ""))
        if draft is None:
            self.draft_status_label.setText("目前沒有草稿。")
            return
        self.draft_status_label.setText(f"已載入草稿 #{draft.id}")

    def go_back(self) -> None:
        if self.parent_mode_select is not None:
            self.parent_mode_select.show()
        self.hide()
