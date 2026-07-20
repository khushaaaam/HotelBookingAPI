from fastapi import FastAPI
from app.routers.bookings import router as booking_router
from app.routers.rooms import router as room_router


app = FastAPI(
    title="Hotel Booking API",
    description="A FastAPI hotel booking API.",
    version="1.0.0",
)

app.include_router(room_router)
app.include_router(booking_router)


@app.get("/")
def root():
    return {
        "Message": "Welcome to the Hotel Booking API.Visit /docs for Swagger UI."
    }