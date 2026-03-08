from __future__ import annotations

from services.draft_service import DraftService
from ui.operation_window_base import OperationWindowBase


class ReturnReceivingWindow(OperationWindowBase):
    def __init__(self, parent_mode_select=None, selected_camera_name: str | None = None, draft_service: DraftService | None = None) -> None:
        super().__init__(
            module_key="returns",
            page_title="退貨收貨",
            page_subtitle="先建立退貨收貨草稿，再記錄退貨原因與外觀檢查。",
            section_title="退貨收貨草稿",
            section_body="目前先保留欄位骨架、相機資訊與草稿功能，後續再接真實退貨流程。",
            form_sections=[
                ("基本資料", ["record_no", "customer_name", "status"]),
                ("退貨資訊", ["updated_at", "notes", "attachments"]),
                ("檢查流程", ["return_reason", "condition_check", "review_tag"]),
            ],
            checklist_items=[
                "先確認單號、客戶名稱與狀態。",
                "退貨原因與外觀檢查先保存為本地草稿。",
                "複核標記與附件欄位會在下一階段接入正式流程。",
            ],
            selected_camera_name=selected_camera_name,
            draft_service=draft_service,
            parent_mode_select=parent_mode_select,
            primary_color="#7c3aed",
            hover_color="#6d28d9",
        )
