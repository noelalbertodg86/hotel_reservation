from fastapi import HTTPException, status


class InvalidValidatorClass(HTTPException):
    def __init__(self, msg: str):
        HTTPException.__init__(self, status_code=status.HTTP_409_CONFLICT, detail=msg)


class ReservationValidatorError(HTTPException):
    def __init__(self, msg: str):
        HTTPException.__init__(self, status_code=status.HTTP_409_CONFLICT, detail=msg)
