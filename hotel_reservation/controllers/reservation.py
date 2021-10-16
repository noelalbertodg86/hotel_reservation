from fastapi import APIRouter

router = APIRouter()


@router.get("/healthcheck", tags=["healthcheck"])
def health_check():
    return {"status": "UP"}
