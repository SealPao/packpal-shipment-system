from __future__ import annotations

from pydantic import BaseModel


class RecordSummary(BaseModel):
    id: str
    record_no: str
    status: str
    customer_name: str
    updated_at: str


class RecordDetail(RecordSummary):
    notes: str
    attachments: list[str]
    tags: list[str]


class RecordListResponse(BaseModel):
    module: str
    items: list[RecordSummary]


class RecordDetailResponse(BaseModel):
    module: str
    item: RecordDetail