from __future__ import annotations

from ui.operation_window_base import OperationWindowBase


class ReturnReceivingWindow(OperationWindowBase):
    def __init__(self, parent_mode_select=None) -> None:
        super().__init__(
            page_title="退貨收貨",
            page_subtitle="此頁面為退貨收貨流程骨架，欄位名稱已先對齊未來 record contract。",
            section_title="預計整合的退貨收貨步驟",
            section_body="先讓退貨頁面與共通 record contract 對齊，後續再補檢查與分類邏輯。",
            form_sections=[
                ("Record Summary", ["record_no", "customer_name", "status"]),
                ("Return Details", ["updated_at", "notes", "attachments"]),
                ("Inspection Workflow", ["return_reason", "condition_check", "review_tag"]),
            ],
            checklist_items=[
                "record_no 對應退貨單號",
                "notes 對應退貨原因與處理備註",
                "attachments 對應照片與佐證文件",
                "status 對應檢查中、待確認或已完成狀態",
            ],
            parent_mode_select=parent_mode_select,
            primary_color="#7c3aed",
            hover_color="#6d28d9",
        )