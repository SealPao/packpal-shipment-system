from __future__ import annotations

from services.draft_service import DraftService
from ui.operation_window_base import OperationWindowBase


class ShipmentWindow(OperationWindowBase):
    def __init__(self, parent_mode_select=None, selected_camera_name: str | None = None, draft_service: DraftService | None = None) -> None:
        super().__init__(
            module_key="shipments",
            page_title="出貨作業",
            page_subtitle="先整理本次出貨資料，再進行拍照、掃碼與後續上傳流程。",
            section_title="出貨資料草稿",
            section_body="這一頁先保留欄位骨架與草稿功能，後續再接 ERP、NAS 與正式 API。",
            form_sections=[
                ("基本資料", ["record_no", "customer_name", "status"]),
                ("出貨內容", ["updated_at", "notes", "attachments"]),
                ("現場流程", ["scan_code", "photo_checkpoint", "upload_queue"]),
            ],
            checklist_items=[
                "先確認單號、客戶名稱與目前狀態。",
                "拍照、附件與上傳佇列目前只保留欄位，不會真正上傳。",
                "需要暫停時可直接儲存草稿，稍後再載入。",
            ],
            selected_camera_name=selected_camera_name,
            draft_service=draft_service,
            parent_mode_select=parent_mode_select,
            primary_color="#0f766e",
            hover_color="#0d5f59",
        )
