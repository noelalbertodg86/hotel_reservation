import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from database import session_factory
from hotel_reservation import config
from hotel_reservation.controllers.reservation_controller import (
    router as reservation_router,
)
from hotel_reservation.controllers.room_controlller import router as room_router
from hotel_reservation.logs import get_logger

logger = get_logger()


def get_session():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
app.include_router(reservation_router)
app.include_router(room_router)


def start():
    uvicorn.run(
        "hotel_reservation.__main__:app",
        host=config.api["host"],
        port=config.api["port"],
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.exception(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"detail": exc.detail}),
    )


@app.exception_handler(Exception)
async def http_exception_handler(request, exc):
    logger.exception(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            {
                "detail": "An internal error has occurred. Check internal logs for details."
            }
        ),
    )


if __name__ == "__main__":
    """Run system endpoints"""
    start()
