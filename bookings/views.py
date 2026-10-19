import sqlite3

from django.shortcuts import render

DB_PATH = "data/restaurant_booking.sqlite"


def bookings(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    bookings_data = conn.execute(
        """
        SELECT
            bookings.id,
            bookings.booking_date,
            tables.number AS table_number,
            tables.capacity,
            users.name AS user_name
        FROM bookings
        JOIN tables
            ON bookings.table_number = tables.number
        JOIN users
            ON bookings.user_id = users.id
        WHERE bookings.is_cancelled = 0
        ORDER BY bookings.booking_date;
        """
    ).fetchall()
    conn.close()
    return render(
        request,
        "bookings/booking_list.html",
        {"bookings": bookings_data},
    )


def booking_detail(request, booking_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    booking = conn.execute(
        """
        SELECT
            bookings.id,
            bookings.booking_date,
            bookings.is_cancelled,
            tables.number AS table_number,
            users.name AS user_name
        FROM bookings
        JOIN tables
            ON bookings.table_number = tables.number
        JOIN users
            ON bookings.user_id = users.id
        WHERE bookings.id = ?;
        """,
        [booking_id],
    ).fetchone()
    conn.close()
    return render(
        request,
        "bookings/booking_detail.html",
        {"booking": booking},
        status=404 if booking is None else 200,
    )


def statistics(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    statistics_data = conn.execute(
        """
        SELECT
            tables.number AS table_number,
            COUNT(bookings.id) AS bookings_count
        FROM tables
        LEFT JOIN bookings
            ON tables.number = bookings.table_number
            AND bookings.is_cancelled = 0
        GROUP BY tables.number
        ORDER BY bookings_count DESC;
        """
    ).fetchall()
    conn.close()
    return render(
        request,
        "bookings/statistics.html",
        {"statistics": statistics_data},
    )
