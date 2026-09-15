from datetime import date
from bookings import is_table_available, create_booking, cancel_booking


def test_is_table_available_empty():
    assert is_table_available([], 1, date(2026, 9, 20)) is True


def test_duplicate_booking_forbidden():
    bookings = []
    create_booking(bookings, 1, date(2026, 9, 20), "Иван")
    assert is_table_available(bookings, 1, date(2026, 9, 20)) is False


def test_booking_on_different_date():
    bookings = []
    create_booking(bookings, 1, date(2026, 9, 20), "Иван")
    assert is_table_available(bookings, 1, date(2026, 9, 21)) is True


def test_cancel_booking():
    bookings = []
    booking = create_booking(bookings, 1, date(2026, 9, 20), "Иван")
    assert cancel_booking(bookings, booking["id"]) is True
    assert is_table_available(bookings, 1, date(2026, 9, 20)) is True
