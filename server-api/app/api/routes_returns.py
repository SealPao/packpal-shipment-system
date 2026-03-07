from fastapi import APIRouter

router = APIRouter(prefix="/returns", tags=["returns"])


@router.get("/placeholder")
async def return_placeholder() -> dict[str, object]:
    return {
        "module": "returns",
        "status": "placeholder",
        "planned_features": [
            "return reason capture",
            "condition inspection workflow",
            "attachment and review workflow",
        ],
    }