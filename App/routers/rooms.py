from uuid import UUID

from fastapi import APIRouter, HTTPException, Response, status

from app.database import bookings_db, rooms_db
from app.models.room import RoomCreate, RoomResponse, RoomUpdate
from app.utils.id_gen import generate_id


router = APIRouter(prefix="/rooms", tags=["Rooms"])


def find_room_by_number(room_number: str, exclude_id: UUID | None = None) -> bool:
    return any(
        room["room_number"] == room_number and room_id != exclude_id
        for room_id, room in rooms_db.items()
    )


@router.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate) -> dict:
    if find_room_by_number(room.room_number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A room with this room_number already exists",
        )

    room_id = generate_id()
    new_room = {"id": room_id, **room.model_dump()}
    rooms_db[room_id] = new_room
    return new_room


@router.get("", response_model=list[RoomResponse], status_code=status.HTTP_200_OK)
def list_rooms() -> list[dict]:
    return list(rooms_db.values())


@router.get("/{room_id}", response_model=RoomResponse, status_code=status.HTTP_200_OK)
def get_room(room_id: UUID) -> dict:
    room = rooms_db.get(room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room


@router.put("/{room_id}", response_model=RoomResponse, status_code=status.HTTP_200_OK)
def replace_room(room_id: UUID, room: RoomCreate) -> dict:
    if room_id not in rooms_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if find_room_by_number(room.room_number, exclude_id=room_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A room with this room_number already exists",
        )

    updated_room = {"id": room_id, **room.model_dump()}
    rooms_db[room_id] = updated_room
    return updated_room


@router.patch("/{room_id}", response_model=RoomResponse, status_code=status.HTTP_200_OK)
def update_room(room_id: UUID, room_update: RoomUpdate) -> dict:
    room = rooms_db.get(room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    changes = room_update.model_dump(exclude_unset=True)
    new_room_number = changes.get("room_number")
    if new_room_number and find_room_by_number(new_room_number, exclude_id=room_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A room with this room_number already exists",
        )

    room.update(changes)
    return room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: UUID) -> Response:
    if room_id not in rooms_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    has_confirmed_booking = any(
        booking["room_id"] == room_id and booking["booking_status"] == "confirmed"
        for booking in bookings_db.values()
    )
    if has_confirmed_booking:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete a room with a confirmed booking",
        )

    del rooms_db[room_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)