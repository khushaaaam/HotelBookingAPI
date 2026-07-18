from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class BookingBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    guest_name: str = Field(..., min_length=2, max_length=100)
    guest_email: EmailStr = Field(...)
    room_id: UUID
    check_in: date = Field(...)
    check_out: date = Field(...)

    @model_validator(mode="after")#tells to run this function after all fields have been validated
    def check_dates(self) -> "BookingBase":
        if self.check_out <= self.check_in:
            raise ValueError("check_out must be after check_in")
        return self


class BookingCreate(BookingBase):
    pass# Inherits all required fields from BookingBase


class BookingUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    guest_name: str | None = Field(default=None, min_length=2, max_length=100)
    guest_email: EmailStr | None = None
    check_in: date | None = None
    check_out: date | None = None


class BookingResponse(BookingBase):
    id: UUID
    booking_status: Literal["confirmed", "cancelled"] = "confirmed"