from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Check service health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
