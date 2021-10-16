import uvicorn
from fastapi import FastAPI

from hotel_reservation import config
from hotel_reservation.controllers.reservation import router as reservation_router

app = FastAPI()
app.include_router(reservation_router)


def start():
    uvicorn.run(
        "hotel_reservation.__main__:app",
        host=config.api["host"],
        port=config.api["port"],
    )


if __name__ == "__main__":
    """Run system endpoints"""
    start()
