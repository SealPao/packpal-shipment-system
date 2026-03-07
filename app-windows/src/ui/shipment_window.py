from __future__ import annotations

from ui.operation_window_base import OperationWindowBase


class ShipmentWindow(OperationWindowBase):
    def __init__(self, parent_mode_select=None) -> None:
        super().__init__(
            page_title="出貨作業",
            page_subtitle="此頁面為出貨流程主畫面骨架，後續將接入掃碼、拍照與資料確認流程。",
            section_title="預計整合的出貨步驟",
            section_body="目前先建立清楚的操作框架，方便後續把資料輸入、相機與本地暫存逐步接上。",
            form_sections=[
                ("基本資料", ["出貨單號", "訂單編號", "客戶名稱"]),
                ("商品資訊", ["商品代碼", "序號 / 條碼", "數量"]),
                ("附件與狀態", ["拍照備註", "待上傳狀態"]),
            ],
            checklist_items=[
                "出貨單號與訂單資訊輸入區",
                "商品條碼或序號掃描區",
                "出貨前拍照與附件區",
                "操作紀錄與待上傳狀態區",
            ],
            parent_mode_select=parent_mode_select,
            primary_color="#0f766e",
            hover_color="#0d5f59",
        )