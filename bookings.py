from datetime import date


def is_table_available(
    bookings: list[dict], table_number: int, booking_date: date
) -> bool:
    for booking in bookings:
        if (
            booking["table_number"] == table_number
            and booking["date"] == booking_date.isoformat()
            and booking["status"] != "Отменено"
        ):
            return False
    return True


def create_booking(
    bookings: list[dict],
    table_number: int,
    booking_date: date,
    client_name: str,
) -> dict | None:
    if not is_table_available(bookings, table_number, booking_date):
        return None

    booking_id = len(bookings) + 1
    booking = {
        "id": booking_id,
        "table_number": table_number,
        "date": booking_date.isoformat(),
        "client_name": client_name,
        "status": "Подтверждено",
    }
    bookings.append(booking)
    return booking


def cancel_booking(bookings: list[dict], booking_id: int) -> bool:
    for booking in bookings:
        if booking["id"] == booking_id and booking["status"] != "Отменено":
            booking["status"] = "Отменено"
            return True
    return False


def get_booking_status(is_available: bool) -> str:
    if is_available:
        return "Столик доступен для бронирования"
    return "Столик уже забронирован"
