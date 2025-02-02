# Hotel Reservation API

## Overview
This is a Django-based API for managing hotel reservations. The system allows users to register, book rooms, make payments, and manage their bookings.

## Features
- User registration and authentication
- Room listing and booking
- Payment processing
- Booking cancellation and updates
- API documentation with Swagger UI

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/hotel-reservation-api.git
   cd hotel-reservation-api
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```sh
   python manage.py migrate
   ```

5. Run the server:
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### Authentication & Users
- `POST /api/v1/users/register/` - Register a new user
- `POST /api/v1/users/login/` - Login a user
- `GET /api/v1/users/` - Get list of users
- `GET /api/v1/users/<uuid:user_id>/` - Get user details

### Bookings
- `POST /api/v1/bookings/create/` - Create a new booking
- `POST /api/v1/bookings/<uuid:booking_id>/pay/` - Make a payment
- `POST /api/v1/bookings/<uuid:booking_id>/confirm_payment/` - Confirm payment
- `GET /api/v1/bookings/<uuid:booking_id>/` - Get booking details
- `POST /api/v1/bookings/<uuid:booking_id>/cancel/` - Cancel a booking
- `PUT /api/v1/bookings/<uuid:booking_id>/update/` - Update booking details
- `GET /api/v1/bookings/list/` - List all bookings
- `GET /api/v1/bookings/transactions/` - List all Transactions
- `GET /api/v1/bookings/transactions/<uuid:transaction_id>/` - List all bookings


### Rooms
- `GET /api/v1/rooms/` - List available rooms
- `GET /api/v1/rooms/<int:room_id>/` - Get room details

### API Documentation
- `GET /schema/` - OpenAPI schema
- `GET /api/v1/docs/` - Swagger UI documentation

