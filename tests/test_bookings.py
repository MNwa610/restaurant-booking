from models import Booking, Table, User
from models.bookings import (
    cancel_booking,
    create_booking,
    is_table_available,
)


def make_table():
    return Table(1, 4, "У окна")


def make_user():
    return User(1, "Иван", "ivan@example.com")


def test_booking_creation():
    table = make_table()
    user = make_user()
    booking = Booking(1, table, "2026-09-20", user)
    assert booking.id == 1
    assert booking.table is table
    assert booking.user is user
    assert booking.booking_date == "2026-09-20"
    assert booking.is_cancelled is False


def test_booking_cancel():
    booking = Booking(1, make_table(), "2026-09-20", make_user())
    booking.cancel()
    assert booking.is_cancelled is True


def test_booking_str():
    booking = Booking(1, make_table(), "2026-09-20", make_user())
    text = str(booking)
    assert "N1" in text
    assert "2026-09-20" in text
    assert "Активно" in text


def test_is_table_available_empty():
    assert is_table_available([], make_table(), "2026-09-20") is True


def test_duplicate_booking_forbidden():
    bookings = []
    table = make_table()
    user = make_user()
    create_booking(bookings, table, "2026-09-20", user)
    assert is_table_available(bookings, table, "2026-09-20") is False


def test_booking_on_different_date():
    bookings = []
    table = make_table()
    user = make_user()
    create_booking(bookings, table, "2026-09-20", user)
    assert is_table_available(bookings, table, "2026-09-21") is True


def test_cancelled_booking_unlocks_table():
    bookings = []
    table = make_table()
    user = make_user()
    booking = create_booking(bookings, table, "2026-09-20", user)
    cancel_booking(bookings, booking.id)
    assert is_table_available(bookings, table, "2026-09-20") is True


def test_cancel_booking_returns_false():
    bookings = []
    assert cancel_booking(bookings, 999) is False
