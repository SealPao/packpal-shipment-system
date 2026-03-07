# PackPal Shipment System - System Spec v1

## 1. Overview
PackPal（出貨小幫手）是一套倉儲影像存證與追溯系統，用於：
- 出貨作業
- 維修收貨
- 退貨收貨

系統由兩部分組成：
1. Windows Portable App
2. NAS Server + Web Admin

---

## 2. Goals
- 建立作業錄影證據
- 建立可搜尋的紀錄
- 降低出貨與收貨爭議
- 保留未來 OCR / 條碼辨識擴充能力

---

## 3. Operating Principle
- 採一人一站
- 每個工作站同時間僅允許一名員工登入
- 每個工作站同時間僅處理一筆作業

---

## 4. Windows App Modes
登入後提供三種作業模式：
- 出貨作業
- 維修收貨
- 退貨收貨

---

## 5. Shipment Flow
1. 員工登入
2. 掃描出貨單號
3. 開始錄影
4. 畫面顯示物流按鈕：
   - 新竹貨運
   - 黑貓
   - 宅配通
   - 郵局
   - 順豐
5. 點選物流商後掃描宅配單號
6. 停止錄影
7. 本地存檔
8. 上傳 NAS

---

## 6. Repair Receiving Flow
1. 員工登入
2. 掃描宅配單號
3. 開始錄影
4. 開箱
5. 可選：掃描設備序號
6. 點選完成開箱
7. 拍攝送修文件
8. 自動文件校正
9. 本地存檔
10. 上傳 NAS

---

## 7. Return Receiving Flow
1. 員工登入
2. 掃描宅配單號
3. 開始錄影
4. 開箱
5. 點選完成開箱
6. 掃描或輸入銷貨單號
7. 本地存檔
8. 上傳 NAS

---

## 8. Document Capture
維修文件拍照需支援：
- 自動偵測四角
- 自動裁切背景
- 自動透視校正
- 同時保留原始照片與校正後照片

文件類型：
- 維修單
- 購買證明
- 保固卡
- 客戶紙條

---

## 9. Windows App Requirements
- Portable one-folder
- Python + PySide6
- OpenCV
- SQLite local storage
- Background upload queue
- Bottom footer must show:

Copyright © 默默工作的小包
有任何問題，請聯繫小包來獲得更多支援，歡迎打賞餵食。

---

## 10. NAS Server Requirements
- FastAPI
- PostgreSQL
- Shared storage for videos and snapshots
- Web Admin for search and management

---

## 11. Web Admin Requirements
可查詢：
- 出貨單號
- 宅配單號
- 日期
- 員工
- 序號

顯示：
- 影片
- 截圖
- 文件照片
- 物流追蹤連結

---

## 12. Versioning
使用 Git + GitHub 管理。

Version format:
- v0.1.0
- v0.2.0
- v1.0.0

Branch strategy:
- main
- develop
- feature/*
