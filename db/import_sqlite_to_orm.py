import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

import django
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "restaurant_booking.settings",
)
django.setup()

from bookings.models import Booking, User  # noqa: E402
from tables.models import Table  # noqa: E402

SOURCE_DB = BASE_DIR / "data" / "restaurant_booking.sqlite"


def get_source_connection():
    conn = sqlite3.connect(SOURCE_DB)
    conn.row_factory = sqlite3.Row
    return conn


def source_count(conn, table_name):
    cursor = conn.execute(f"SELECT COUNT(*) AS cnt FROM {table_name}")
    return cursor.fetchone()["cnt"]


def import_tables(conn):
    rows = conn.execute("SELECT * FROM tables ORDER BY number")
    for row in rows:
        Table.objects.update_or_create(
            pk=row["number"],
            defaults={
                "capacity": row["capacity"],
                "location": row["location"],
            },
        )


def import_users(conn):
    rows = conn.execute("SELECT * FROM users ORDER BY id")
    for row in rows:
        User.objects.update_or_create(
            pk=row["id"],
            defaults={
                "name": row["name"],
                "email": row["email"],
            },
        )


def import_bookings(conn):
    rows = conn.execute("SELECT * FROM bookings ORDER BY id")
    for row in rows:
        Booking.objects.update_or_create(
            pk=row["id"],
            defaults={
                "table_id": row["table_number"],
                "user_id": row["user_id"],
                "booking_date": date.fromisoformat(row["booking_date"]),
                "is_cancelled": bool(row["is_cancelled"]),
            },
        )


def compare_counts(conn):
    print("Сравнение количества записей:")
    print(
        f"  tables: source={source_count(conn, 'tables')} "
        f"orm={Table.objects.count()}"
    )
    print(
        f"  users: source={source_count(conn, 'users')} "
        f"orm={User.objects.count()}"
    )
    print(
        f"  bookings: source={source_count(conn, 'bookings')} "
        f"orm={Booking.objects.count()}"
    )


def show_relations():
    print("Связи через select_related:")
    bookings = Booking.objects.select_related("table", "user").all()
    for booking in bookings:
        print(
            f"  #{booking.id}: столик N{booking.table.number}, "
            f"{booking.user.name}, {booking.booking_date}, "
            f"отменено={booking.is_cancelled}"
        )


def main():
    conn = get_source_connection()
    try:
        with transaction.atomic():
            import_tables(conn)
            import_users(conn)
            import_bookings(conn)
        compare_counts(conn)
        show_relations()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
