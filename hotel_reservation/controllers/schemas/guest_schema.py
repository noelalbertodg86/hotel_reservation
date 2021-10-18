import re
from fastapi import HTTPException
from typing import Optional

from pydantic import BaseModel, validator


class Guest(BaseModel):
    id: str
    full_name: str
    email: str
    phone_number: Optional[str]

    @validator("email")
    def validate_email(cls, email: str):
        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(email_regex, email):
            return email
        raise HTTPException(status_code=400, detail="Invalid email address")

    @validator("phone_number")
    def validate_phone_number(cls, phone_number: str):
        phone_regex = r"^[0-9\-\+]{9,15}$"
        if re.fullmatch(phone_regex, phone_number):
            return phone_number
        raise HTTPException(status_code=400, detail="Invalid phone number")
