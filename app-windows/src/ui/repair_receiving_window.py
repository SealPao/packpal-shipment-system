from __future__ import annotations

from ui.operation_window_base import OperationWindowBase


class RepairReceivingWindow(OperationWindowBase):
    def __init__(self, parent_mode_select=None) -> None:
        super().__init__(
            page_title="維修收貨",
            page_subtitle="此頁面為維修收貨流程骨架，後續將接入收件資訊、故障描述與文件拍攝。",
            section_title="預計整合的維修收貨步驟",
            section_body="先把操作入口和頁面節奏固定，之後再補實際欄位、附件與上傳任務。",
            checklist_items=[
                "收貨單號與客戶資料輸入區",
                "商品外觀與序號記錄區",
                "故障描述與備註欄位",
                "文件拍攝與附件檢查區",
            ],
            parent_mode_select=parent_mode_select,
            primary_color="#b45309",
            hover_color="#92400e",
        )