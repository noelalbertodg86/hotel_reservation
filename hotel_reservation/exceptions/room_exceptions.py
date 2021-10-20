from fastapi import HTTPException, status


class NotFoundRoomError(HTTPException):
    def __init__(self, room_id: int):
        msg = f"Room with number:{room_id} Not Found"
        HTTPException.__init__(self, status_code=status.HTTP_404_NOT_FOUND, detail=msg)
