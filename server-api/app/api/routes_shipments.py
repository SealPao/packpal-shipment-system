from fastapi import APIRouter, HTTPException

from app.schemas.records import RecordDetailResponse, RecordListResponse
from app.services.placeholder_records import get_record, list_records

router = APIRouter(prefix="/shipments", tags=["shipments"])


@router.get("", response_model=RecordListResponse)
async def shipment_list() -> RecordListResponse:
    return RecordListResponse(module="shipments", items=list_records("shipments"))


@router.get("/{record_id}", response_model=RecordDetailResponse)
async def shipment_detail(record_id: str) -> RecordDetailResponse:
    record = get_record("shipments", record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Shipment record not found")

    return RecordDetailResponse(module="shipments", item=record)