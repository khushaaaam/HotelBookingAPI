from uuid import UUID

from fastapi import APIRouter, HTTPException, Response, status

from app.database import bookings_db, rooms_db
from app.models.booking import BookingCreate, BookingResponse, BookingUpdate
from app.utils.id_gen import generate_id


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate) -> dict:
    room = rooms_db.get(booking.room_id)

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    if not room["is_available"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room is not available",
        )

    booking_id = generate_id()

    new_booking = {
        "id": booking_id,
        **booking.model_dump(),
        "booking_status": "confirmed",
    }

    bookings_db[booking_id] = new_booking
    room["is_available"] = False

    return new_booking


@router.get("", response_model=list[BookingResponse])
def list_bookings() -> list[dict]:
    return list(bookings_db.values())


@router.post("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(booking_id: UUID) -> dict:
    booking = bookings_db.get(booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    booking["booking_status"] = "cancelled"
    rooms_db[booking["room_id"]]["is_available"] = True

    return booking


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: UUID) -> dict:
    booking = bookings_db.get(booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    return booking


@router.put("/{booking_id}", response_model=BookingResponse)
def replace_booking(booking_id: UUID, booking: BookingCreate) -> dict:
    stored_booking = bookings_db.get(booking_id)

    if stored_booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    if booking.room_id != stored_booking["room_id"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Changing the room is not supported",
        )

    updated_booking = {
        "id": booking_id,
        **booking.model_dump(),
        "booking_status": stored_booking["booking_status"],
    }

    bookings_db[booking_id] = updated_booking

    return updated_booking


@router.patch("/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: UUID, booking_update: BookingUpdate) -> dict:
    booking = bookings_db.get(booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    changes = booking_update.model_dump(exclude_unset=True)
    candidate = {**booking, **changes}

    BookingCreate.model_validate(candidate)

    booking.update(changes)

    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: UUID) -> Response:
    booking = bookings_db.get(booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    rooms_db[booking["room_id"]]["is_available"] = True

    del bookings_db[booking_id]

    return Response(status_code=status.HTTP_204_NO_CONTENT)