from __future__ import annotations

from services.draft_service import DraftService
from ui.operation_window_base import OperationWindowBase


class RepairReceivingWindow(OperationWindowBase):
    def __init__(self, parent_mode_select=None, selected_camera_name: str | None = None, draft_service: DraftService | None = None) -> None:
        super().__init__(
            module_key="repairs",
            page_title="維修收貨",
            page_subtitle="先建立維修收貨草稿，再補拍照、序號與文件檢查。",
            section_title="維修收貨草稿",
            section_body="後續會接正式維修收貨流程；目前先整理欄位、相機與草稿保存能力。",
            form_sections=[
                ("基本資料", ["record_no", "customer_name", "status"]),
                ("維修資訊", ["updated_at", "notes", "attachments"]),
                ("收貨檢查", ["device_serial", "issue_summary", "document_check"]),
            ],
            checklist_items=[
                "先確認單號、客戶名稱與狀態。",
                "設備序號、問題摘要與文件檢查先保存為本地草稿。",
                "附件與拍照串接會在下一階段接入。",
            ],
            selected_camera_name=selected_camera_name,
            draft_service=draft_service,
            parent_mode_select=parent_mode_select,
            primary_color="#b45309",
            hover_color="#92400e",
        )
