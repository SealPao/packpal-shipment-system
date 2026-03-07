from __future__ import annotations

from services.draft_service import DraftService
from ui.operation_window_base import OperationWindowBase


class ShipmentWindow(OperationWindowBase):
    def __init__(
        self,
        parent_mode_select=None,
        selected_camera_name: str | None = None,
        draft_service: DraftService | None = None,
    ) -> None:
        super().__init__(
            module_key="shipments",
            page_title="出貨作業",
            page_subtitle="此頁面為出貨流程主畫面骨架，欄位名稱已先對齊未來 record contract。",
            section_title="預計整合的出貨步驟",
            section_body="目前先建立與後端契約接近的欄位語意，之後接資料與上傳流程時可以直接映射。",
            form_sections=[
                ("Record Summary", ["record_no", "customer_name", "status"]),
                ("Shipment Details", ["updated_at", "notes", "attachments"]),
                ("Local Workflow", ["scan_code", "photo_checkpoint", "upload_queue"]),
            ],
            checklist_items=[
                "record_no 對應出貨單號或單據編號",
                "customer_name 對應客戶或通路名稱",
                "attachments 對應拍照與附檔清單",
                "status 對應本地處理與上傳狀態",
            ],
            selected_camera_name=selected_camera_name,
            draft_service=draft_service,
            parent_mode_select=parent_mode_select,
            primary_color="#0f766e",
            hover_color="#0d5f59",
        )