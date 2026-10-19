import sqlite3
from datetime import date

from django.shortcuts import render

DB_PATH = "data/restaurant_booking.sqlite"


def tables(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    tables_list = conn.execute(
        """
        SELECT
            number,
            capacity,
            location
        FROM tables
        ORDER BY number;
        """
    ).fetchall()
    conn.close()
    return render(
        request,
        "tables/table_list.html",
        {"tables": tables_list},
    )


def table_detail(request, table_number):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    table = conn.execute(
        """
        SELECT
            number,
            capacity,
            location
        FROM tables
        WHERE number = ?;
        """,
        [table_number],
    ).fetchone()
    available = False
    if table is not None:
        free_table = conn.execute(
            """
            SELECT
                tables.number
            FROM tables
            WHERE tables.number = ?
                AND tables.number NOT IN (
                    SELECT bookings.table_number
                    FROM bookings
                    WHERE bookings.booking_date = ?
                        AND bookings.is_cancelled = 0
                );
            """,
            [table_number, date.today().isoformat()],
        ).fetchone()
        available = free_table is not None
    conn.close()
    return render(
        request,
        "tables/table_detail.html",
        {
            "table": table,
            "available": available,
        },
        status=404 if table is None else 200,
    )


def available_tables(request):
    booking_date = request.GET.get("date")
    tables_list = []
    if booking_date:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        tables_list = conn.execute(
            """
            SELECT
                tables.number,
                tables.capacity,
                tables.location
            FROM tables
            WHERE tables.number NOT IN (
                SELECT bookings.table_number
                FROM bookings
                WHERE bookings.booking_date = ?
                    AND bookings.is_cancelled = 0
            )
            ORDER BY tables.number;
            """,
            [booking_date],
        ).fetchall()
        conn.close()
    return render(
        request,
        "tables/available.html",
        {
            "tables": tables_list,
            "booking_date": booking_date,
        },
    )
