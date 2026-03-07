from __future__ import annotations

from typing import Iterable, Sequence

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from services.draft_service import DraftService
from ui.common import ScreenContainer, app_stylesheet, build_footer, create_back_row, create_card, create_page_header


class OperationWindowBase(QMainWindow):
    def __init__(
        self,
        *,
        module_key: str,
        page_title: str,
        page_subtitle: str,
        section_title: str,
        section_body: str,
        checklist_items: Iterable[str],
        form_sections: Sequence[tuple[str, list[str]]],
        selected_camera_name: str | None = None,
        draft_service: DraftService | None = None,
        parent_mode_select: QMainWindow | None = None,
        primary_color: str = "#2563eb",
        hover_color: str = "#1d4ed8",
    ) -> None:
        super().__init__(parent_mode_select)
        self.module_key = module_key
        self.parent_mode_select = parent_mode_select
        self.selected_camera_name = selected_camera_name or ""
        self.draft_service = draft_service or DraftService()
        self.fields: dict[str, QLineEdit] = {}

        self.setWindowTitle(f"{APP_TITLE} - {page_title}")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        container = ScreenContainer()
        self.setCentralWidget(container)

        container.layout.addStretch(1)
        container.layout.addWidget(create_page_header(page_title, page_subtitle))

        card, card_layout = create_card()
        card_layout.addWidget(self._build_section_title(section_title))
        card_layout.addWidget(self._build_section_body(section_body))
        card_layout.addWidget(self._build_camera_status())
        card_layout.addWidget(self._build_draft_toolbar())

        for section_title_text, field_keys in form_sections:
            card_layout.addWidget(self._build_form_section(section_title_text, field_keys))

        for item in checklist_items:
            card_layout.addWidget(self._build_bullet(item))

        back_row, back_button = create_back_row()
        back_button.clicked.connect(self.go_back)
        card_layout.addSpacing(8)
        card_layout.addWidget(back_row)

        container.layout.addWidget(card)
        container.layout.addStretch(1)
        container.layout.addWidget(build_footer())

        self.load_latest_draft(show_empty_message=False)
        self.setStyleSheet(app_stylesheet(primary_color, hover_color))

    def _build_section_title(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("sectionTitle")
        return label

    def _build_section_body(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("sectionBody")
        label.setWordWrap(True)
        return label

    def _build_camera_status(self) -> QLabel:
        label = QLabel(f"目前選擇的相機：{self.selected_camera_name or '未選擇'}")
        label.setObjectName("cameraStatus")
        return label

    def _build_draft_toolbar(self) -> QWidget:
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        save_button = QPushButton("儲存草稿")
        save_button.clicked.connect(self.save_draft)

        load_button = QPushButton("載入最近草稿")
        load_button.setObjectName("secondaryButton")
        load_button.clicked.connect(lambda: self.load_latest_draft(show_empty_message=True))

        self.draft_status_label = QLabel("尚未儲存草稿")
        self.draft_status_label.setObjectName("draftStatus")

        layout.addWidget(save_button)
        layout.addWidget(load_button)
        layout.addWidget(self.draft_status_label, 1)
        return row

    def _build_form_section(self, title_text: str, field_keys: list[str]) -> QFrame:
        section = QFrame()
        section.setObjectName("subCard")
        layout = QVBoxLayout(section)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel(title_text)
        title.setObjectName("subSectionTitle")
        layout.addWidget(title)

        for field_key in field_keys:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(12)

            label = QLabel(field_key)
            label.setObjectName("fieldLabel")
            label.setMinimumWidth(180)

            field = QLineEdit()
            field.setObjectName("placeholderField")
            field.setPlaceholderText(f"預留欄位：{field_key}")
            self.fields[field_key] = field

            row_layout.addWidget(label)
            row_layout.addWidget(field, 1)
            layout.addWidget(row)

        return section

    def _build_bullet(self, text: str) -> QWidget:
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        bullet = QLabel("-")
        bullet.setObjectName("sectionBody")

        content = QLabel(text)
        content.setObjectName("sectionBody")
        content.setWordWrap(True)

        layout.addWidget(bullet)
        layout.addWidget(content, 1)
        return row

    def collect_form_data(self) -> dict[str, str]:
        return {field_key: widget.text().strip() for field_key, widget in self.fields.items()}

    def save_draft(self) -> None:
        draft_id = self.draft_service.save_draft(
            module_key=self.module_key,
            payload=self.collect_form_data(),
            camera_name=self.selected_camera_name,
        )
        self.draft_status_label.setText(f"草稿已儲存 #{draft_id}")

    def load_latest_draft(self, show_empty_message: bool) -> None:
        draft = self.draft_service.latest_draft(self.module_key)
        payload = self.draft_service.parse_payload(draft)

        if draft is None:
            if show_empty_message:
                self.draft_status_label.setText("目前沒有可用草稿")
            return

        for field_key, widget in self.fields.items():
            widget.setText(payload.get(field_key, ""))

        camera_name = draft.camera_name or self.selected_camera_name or "未選擇"
        self.draft_status_label.setText(f"已載入草稿 #{draft.id} / 相機：{camera_name}")

    def go_back(self) -> None:
        if self.parent_mode_select is not None:
            self.parent_mode_select.show()
        self.close()