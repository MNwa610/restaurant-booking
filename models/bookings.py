from typing import Optional

from .tables import Table
from .users import User


class Booking:
    def __init__(
        self,
        booking_id: int,
        table: Table,
        booking_date: str,
        user: User,
    ) -> None:
        self.id = booking_id
        self.table = table
        self.booking_date = booking_date
        self.user = user
        self.is_cancelled = False

    def cancel(self) -> None:
        self.is_cancelled = True

    def __str__(self) -> str:
        status = "Отменено" if self.is_cancelled else "Активно"
        return (
            f"Бронирование #{self.id} | "
            f"{self.table} | "
            f"{self.booking_date} | "
            f"{self.user.name} | "
            f"{status}"
        )


def is_table_available(
    bookings: list[Booking],
    table: Table,
    booking_date: str,
) -> bool:
    for booking in bookings:
        if (
            booking.table.number == table.number
            and booking.booking_date == booking_date
            and not booking.is_cancelled
        ):
            return False
    return True


def create_booking(
    bookings: list[Booking],
    table: Table,
    booking_date: str,
    user: User,
) -> Optional[Booking]:
    if not is_table_available(bookings, table, booking_date):
        return None

    booking_id = len(bookings) + 1
    booking = Booking(booking_id, table, booking_date, user)
    bookings.append(booking)
    return booking


def cancel_booking(bookings: list[Booking], booking_id: int) -> bool:
    for booking in bookings:
        if booking.id == booking_id and not booking.is_cancelled:
            booking.cancel()
            return True
    return False


def get_booking_status(is_available: bool) -> str:
    if is_available:
        return "Столик доступен для бронирования"
    return "Столик уже забронирован"


def show_bookings(bookings: list[Booking]) -> None:
    if not bookings:
        print("Бронирований пока нет.")
        return

    print("\nБронирования:")
    print("-" * 70)
    for booking in bookings:
        print(f"  {booking}")
    print("-" * 70)
