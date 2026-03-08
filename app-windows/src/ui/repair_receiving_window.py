from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from services.draft_service import DraftService
from ui.common import ScreenContainer, app_stylesheet, apply_window_icon, show_window_like


class RepairReceivingWindow(QMainWindow):
    def __init__(self, parent_mode_select=None, selected_camera_name: str | None = None, draft_service: DraftService | None = None) -> None:
        super().__init__(parent_mode_select)
        self.parent_mode_select = parent_mode_select
        self.selected_camera_name = selected_camera_name or "尚未選擇"
        self.draft_service = draft_service or DraftService()

        self.setWindowTitle(f"{APP_TITLE} - 維修收貨")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        apply_window_icon(self)

        container = ScreenContainer()
        container.layout.setContentsMargins(0, 0, 0, 0)
        container.layout.setSpacing(0)
        self.setCentralWidget(container)

        stage = QFrame()
        stage.setObjectName("cameraStage")
        stage_layout = QVBoxLayout(stage)
        stage_layout.setContentsMargins(24, 24, 24, 24)
        stage_layout.setSpacing(0)

        top_overlay = QHBoxLayout()
        top_overlay.setSpacing(12)
        title = QLabel("維修收貨")
        title.setStyleSheet("color: white; font-size: 28px; font-weight: 700;")
        camera_label = QLabel(f"相機：{self.selected_camera_name}")
        camera_label.setStyleSheet("color: white; font-size: 14px; background: rgba(15,23,42,0.45); padding: 8px 12px; border-radius: 12px;")
        top_overlay.addWidget(title)
        top_overlay.addStretch(1)
        top_overlay.addWidget(camera_label)
        stage_layout.addLayout(top_overlay)

        stage_layout.addStretch(1)

        center_prompt = QLabel("請掃描維修單號開始收貨")
        center_prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_prompt.setStyleSheet("color: white; font-size: 34px; font-weight: 700;")
        stage_layout.addWidget(center_prompt)

        sub_prompt = QLabel("正式版會在這裡顯示相機畫面、設備序號與問題摘要收集流程。")
        sub_prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_prompt.setStyleSheet("color: rgba(255,255,255,0.82); font-size: 16px;")
        stage_layout.addWidget(sub_prompt)

        stage_layout.addStretch(1)

        bottom_overlay = QVBoxLayout()
        bottom_overlay.setSpacing(12)

        self.scan_input = QLineEdit()
        self.scan_input.setPlaceholderText("請掃描或輸入維修單號")
        self.scan_input.setMinimumHeight(56)
        self.scan_input.setStyleSheet("font-size: 24px; background: rgba(255,255,255,0.96);")
        bottom_overlay.addWidget(self.scan_input)

        action_row = QHBoxLayout()
        action_row.setSpacing(12)
        back_button = QPushButton("返回模式選擇")
        back_button.setObjectName("secondaryButton")
        back_button.clicked.connect(self.go_back)
        load_button = QPushButton("載入最近草稿")
        load_button.setObjectName("secondaryButton")
        load_button.clicked.connect(self.load_latest_draft)
        save_button = QPushButton("儲存草稿")
        save_button.clicked.connect(self.save_draft)
        self.draft_status_label = QLabel("尚未儲存草稿")
        self.draft_status_label.setStyleSheet("color: white; font-size: 14px;")
        action_row.addWidget(back_button)
        action_row.addWidget(load_button)
        action_row.addWidget(save_button)
        action_row.addStretch(1)
        action_row.addWidget(self.draft_status_label)
        bottom_overlay.addLayout(action_row)
        stage_layout.addLayout(bottom_overlay)

        container.layout.addWidget(stage)
        self.load_latest_draft()
        self.setStyleSheet(app_stylesheet("#b45309", "#92400e") + "QFrame#cameraStage { background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #422006, stop:1 #92400e); }")

    def closeEvent(self, event: QCloseEvent) -> None:
        app = QApplication.instance()
        if app is not None:
            app.quit()
        event.accept()

    def save_draft(self) -> None:
        draft_id = self.draft_service.save_draft(
            module_key="repairs",
            payload={"record_no": self.scan_input.text().strip()},
            camera_name=self.selected_camera_name,
        )
        self.draft_status_label.setText(f"草稿已儲存，編號 #{draft_id}")

    def load_latest_draft(self) -> None:
        draft = self.draft_service.latest_draft("repairs")
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

