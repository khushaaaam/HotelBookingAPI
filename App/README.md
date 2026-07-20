# 🏨 Hotel Booking API

A RESTful Hotel Booking API built with **FastAPI**, **Pydantic**, and **UUIDs**. This project demonstrates CRUD operations, request validation, business logic implementation, and automatic API documentation using Swagger UI.

> **Note:** This project uses an in-memory Python dictionary as the database, so all data is lost when the server restarts.

---

## ✨ Features

- 🛏️ Complete CRUD operations for Rooms
- 📅 Complete CRUD operations for Bookings
- 🔑 UUID-based resource identification
- ✅ Request and response validation with Pydantic
- 📖 Interactive Swagger API documentation
- 🔄 Automatic room availability management
- ⚡ FastAPI-powered REST API
- 💾 In-memory database using Python dictionaries

---

## 🛠️ Tech Stack

- Python 3.x
- FastAPI
- Pydantic
- Uvicorn
- UUID
- Python Dictionaries (In-Memory Storage)

---

## 📂 Project Structure

```text
HotelBookingAPI/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   ├── room.py
│   │   └── booking.py
│   ├── routers/
│   │   ├── rooms.py
│   │   └── bookings.py
│   └── utils/
│       └── id_gen.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/HotelBookingAPI.git
cd HotelBookingAPI
```

### 2. Create a virtual environment

```bash
py -m venv .venv
```

### 3. Activate the virtual environment

**Windows (PowerShell)**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

## 📚 API Documentation

FastAPI automatically generates interactive API documentation.

| Documentation | URL |
|--------------|-----|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

---

# 📌 API Endpoints

## 🛏️ Rooms

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/rooms` | Create a room |
| GET | `/rooms` | Retrieve all rooms |
| GET | `/rooms/{room_id}` | Retrieve a room by ID |
| PUT | `/rooms/{room_id}` | Replace a room |
| PATCH | `/rooms/{room_id}` | Partially update a room |
| DELETE | `/rooms/{room_id}` | Delete a room |

---

## 📅 Bookings

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/bookings` | Create a booking |
| GET | `/bookings` | Retrieve all bookings |
| GET | `/bookings/{booking_id}` | Retrieve a booking by ID |
| PUT | `/bookings/{booking_id}` | Replace a booking |
| PATCH | `/bookings/{booking_id}` | Partially update a booking |
| POST | `/bookings/{booking_id}/cancel` | Cancel a booking |
| DELETE | `/bookings/{booking_id}` | Delete a booking |

---

# 📥 Example Requests

## Create a Room

```json
{
  "room_number": "101",
  "room_type": "Deluxe",
  "price_per_night": 1000,
  "capacity": 2,
  "is_available": true
}
```

---

## Create a Booking

```json
{
  "guest_name": "alex",
  "guest_email": "alex@example.com",
  "room_id": "PASTE_ROOM_UUID_HERE",
  "check_in": "2026-08-10",
  "check_out": "2026-08-13"
}
```

---

# 📋 Business Rules

- A booking can only be created for an existing room.
- A room must be available before it can be booked.
- Creating a booking automatically marks the room as unavailable.
- Cancelling or deleting a confirmed booking automatically makes the room available again.
- The check-out date must be later than the check-in date.

---

# 🎯 Learning Objectives

This project demonstrates:

- Building REST APIs with FastAPI
- Request validation using Pydantic
- CRUD API design
- UUID-based resource management
- API routing and modular project structure
- Business rule implementation
- Proper HTTP status codes and error handling
- Interactive API documentation with Swagger

---

# ⚠️ Limitations

- Uses an in-memory database (no persistent storage)
- Data is lost when the server restarts
- Authentication and authorization are not implemented
- Not intended for production use

---

## 👨‍💻 Author

Built as a backend learning project using **FastAPI** to practice REST API development, validation, routing, and business logic implementation.