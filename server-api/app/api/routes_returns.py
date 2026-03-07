from fastapi import APIRouter, HTTPException

from app.schemas.records import RecordDetailResponse, RecordListResponse
from app.services.placeholder_records import get_record, list_records

router = APIRouter(prefix="/returns", tags=["returns"])


@router.get("", response_model=RecordListResponse)
async def return_list() -> RecordListResponse:
    return RecordListResponse(module="returns", items=list_records("returns"))


@router.get("/{record_id}", response_model=RecordDetailResponse)
async def return_detail(record_id: str) -> RecordDetailResponse:
    record = get_record("returns", record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Return record not found")

    return RecordDetailResponse(module="returns", item=record)