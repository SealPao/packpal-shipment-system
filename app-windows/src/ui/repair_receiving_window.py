from __future__ import annotations

from ui.operation_window_base import OperationWindowBase


class RepairReceivingWindow(OperationWindowBase):
    def __init__(self, parent_mode_select=None) -> None:
        super().__init__(
            page_title="維修收貨",
            page_subtitle="此頁面為維修收貨流程骨架，欄位名稱已先對齊未來 record contract。",
            section_title="預計整合的維修收貨步驟",
            section_body="先以共通 record contract 命名收斂，再逐步補上維修流程專有欄位。",
            form_sections=[
                ("Record Summary", ["record_no", "customer_name", "status"]),
                ("Repair Details", ["updated_at", "notes", "attachments"]),
                ("Intake Workflow", ["device_serial", "issue_summary", "document_check"]),
            ],
            checklist_items=[
                "record_no 對應維修收貨單號",
                "notes 對應故障描述與收件備註",
                "attachments 對應文件與外觀照片",
                "status 對應收件、待補件或待確認狀態",
            ],
            parent_mode_select=parent_mode_select,
            primary_color="#b45309",
            hover_color="#92400e",
        )