from __future__ import annotations

from app.schemas.records import RecordDetail, RecordSummary


_PLACEHOLDER_DATA = {
    "shipments": [
        RecordDetail(
            id="shipment-001",
            record_no="SHP-2026-0001",
            status="draft",
            customer_name="北區門市",
            updated_at="2026-03-08T09:00:00+08:00",
            notes="等待條碼掃描與附件補齊。",
            attachments=["front-photo", "packing-slip"],
            tags=["shipment", "pending-upload"],
        ),
        RecordDetail(
            id="shipment-002",
            record_no="SHP-2026-0002",
            status="queued",
            customer_name="南區經銷商",
            updated_at="2026-03-08T10:30:00+08:00",
            notes="已完成基本資料，待上傳 NAS。",
            attachments=["box-photo"],
            tags=["shipment"],
        ),
    ],
    "repairs": [
        RecordDetail(
            id="repair-001",
            record_no="RPR-2026-0001",
            status="received",
            customer_name="王小明",
            updated_at="2026-03-08T11:00:00+08:00",
            notes="待補故障描述附件。",
            attachments=["device-photo", "service-form"],
            tags=["repair", "intake"],
        )
    ],
    "returns": [
        RecordDetail(
            id="return-001",
            record_no="RTN-2026-0001",
            status="inspection",
            customer_name="線上商城",
            updated_at="2026-03-08T12:00:00+08:00",
            notes="商品外箱有破損，待確認退貨原因。",
            attachments=["damage-photo"],
            tags=["return", "inspection"],
        )
    ],
}


def _matches(record: RecordDetail, q: str | None = None, status: str | None = None) -> bool:
    if status and record.status != status:
        return False

    if q:
        keyword = q.lower()
        haystacks = [
            record.record_no,
            record.customer_name,
            record.notes,
            *record.tags,
        ]
        if not any(keyword in value.lower() for value in haystacks):
            return False

    return True


def list_records(module: str, q: str | None = None, status: str | None = None) -> list[RecordSummary]:
    return [
        RecordSummary(**item.model_dump(include={"id", "record_no", "status", "customer_name", "updated_at"}))
        for item in _PLACEHOLDER_DATA[module]
        if _matches(item, q=q, status=status)
    ]



def get_record(module: str, record_id: str) -> RecordDetail | None:
    for item in _PLACEHOLDER_DATA[module]:
        if item.id == record_id:
            return item
    return None