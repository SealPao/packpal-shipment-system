from __future__ import annotations

from ui.operation_window_base import OperationWindowBase


class ReturnReceivingWindow(OperationWindowBase):
    def __init__(self, parent_mode_select=None) -> None:
        super().__init__(
            page_title="退貨收貨",
            page_subtitle="此頁面為退貨收貨流程骨架，後續將接入退貨原因、檢查狀態與附件整理。",
            section_title="預計整合的退貨收貨步驟",
            section_body="先保留完整頁面骨架，讓後續的退貨檢查、分類與證據附件能直接填進來。",
            checklist_items=[
                "退貨單號與來源資訊輸入區",
                "商品狀態檢查與分類區",
                "退貨原因與備註欄位",
                "附件拍攝與後續處理標記區",
            ],
            parent_mode_select=parent_mode_select,
            primary_color="#7c3aed",
            hover_color="#6d28d9",
        )