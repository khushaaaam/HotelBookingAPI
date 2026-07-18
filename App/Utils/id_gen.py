from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RoomBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)#removes whitespaces

    room_number: str = Field(..., min_length=1, max_length=10, examples=["101"])
    room_type: str = Field(..., min_length=2, max_length=50, examples=["Deluxe"])
    price_per_night: float = Field(..., gt=0, examples=[1000.00])
    capacity: int = Field(..., gt=0, examples=[2])
    is_available: bool = True


class RoomCreate(RoomBase):
    pass# Inherits all required fields from RoomBase


class RoomUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    room_number: str | None = Field(default=None, min_length=1, max_length=10)
    room_type: str | None = Field(default=None, min_length=2, max_length=50)
    price_per_night: float | None = Field(default=None, gt=0)
    capacity: int | None = Field(default=None, gt=0)
    is_available: bool | None = None


class RoomResponse(RoomBase):
    id: UUID