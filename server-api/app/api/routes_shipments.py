from fastapi import APIRouter

router = APIRouter(prefix="/shipments", tags=["shipments"])


@router.get("/placeholder")
async def shipment_placeholder() -> dict[str, object]:
    return {
        "module": "shipments",
        "status": "placeholder",
        "planned_features": [
            "shipment record intake",
            "scan and attachment workflow",
            "upload queue integration",
        ],
    }