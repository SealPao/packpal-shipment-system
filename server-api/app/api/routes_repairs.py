from fastapi import APIRouter, HTTPException

from app.schemas.records import RecordDetailResponse, RecordListResponse
from app.services.placeholder_records import get_record, list_records

router = APIRouter(prefix="/repairs", tags=["repairs"])


@router.get("", response_model=RecordListResponse)
async def repair_list() -> RecordListResponse:
    return RecordListResponse(module="repairs", items=list_records("repairs"))


@router.get("/{record_id}", response_model=RecordDetailResponse)
async def repair_detail(record_id: str) -> RecordDetailResponse:
    record = get_record("repairs", record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Repair record not found")

    return RecordDetailResponse(module="repairs", item=record)