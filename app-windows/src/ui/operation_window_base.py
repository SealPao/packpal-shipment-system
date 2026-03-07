from __future__ import annotations

from typing import Iterable

from PySide6.QtWidgets import QLabel, QMainWindow, QWidget

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from ui.common import (
    ScreenContainer,
    app_stylesheet,
    build_footer,
    create_back_row,
    create_card,
    create_page_header,
)


class OperationWindowBase(QMainWindow):
    def __init__(
        self,
        *,
        page_title: str,
        page_subtitle: str,
        section_title: str,
        section_body: str,
        checklist_items: Iterable[str],
        parent_mode_select: QMainWindow | None = None,
        primary_color: str = "#2563eb",
        hover_color: str = "#1d4ed8",
    ) -> None:
        super().__init__(parent_mode_select)
        self.parent_mode_select = parent_mode_select

        self.setWindowTitle(f"{APP_TITLE} - {page_title}")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        container = ScreenContainer()
        self.setCentralWidget(container)

        container.layout.addStretch(1)
        container.layout.addWidget(create_page_header(page_title, page_subtitle))

        card, card_layout = create_card()
        card_layout.addWidget(self._build_section_title(section_title))
        card_layout.addWidget(self._build_section_body(section_body))

        for item in checklist_items:
            card_layout.addWidget(self._build_bullet(item))

        back_row, back_button = create_back_row()
        back_button.clicked.connect(self.go_back)
        card_layout.addSpacing(8)
        card_layout.addWidget(back_row)

        container.layout.addWidget(card)
        container.layout.addStretch(1)
        container.layout.addWidget(build_footer())

        self.setStyleSheet(app_stylesheet(primary_color, hover_color))

    def go_back(self) -> None:
        if self.parent_mode_select is not None:
            self.parent_mode_select.show()
        self.close()

    def _build_section_title(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("sectionTitle")
        return label

    def _build_section_body(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("sectionBody")
        label.setWordWrap(True)
        return label

    def _build_bullet(self, text: str) -> QWidget:
        row = QWidget()
        from PySide6.QtWidgets import QHBoxLayout

        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        bullet = QLabel("•")
        bullet.setObjectName("sectionBody")

        content = QLabel(text)
        content.setObjectName("sectionBody")
        content.setWordWrap(True)

        layout.addWidget(bullet)
        layout.addWidget(content, 1)
        return row