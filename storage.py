import json
from pathlib import Path

from models import Booking, Table, User
from models.tables import find_table_by_number
from models.users import find_user_by_id


def load_tables(filename: str) -> list[Table]:
    path = Path(filename)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return [
                Table(
                    table_number=item["number"],
                    capacity=item["capacity"],
                    location=item["location"],
                )
                for item in data
            ]
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"Ошибка чтения файла {filename}: {error}")
        return []


def save_tables(filename: str, tables: list[Table]) -> None:
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [
                    {
                        "number": table.number,
                        "capacity": table.capacity,
                        "location": table.location,
                    }
                    for table in tables
                ],
                file,
                ensure_ascii=False,
                indent=2,
            )
    except OSError as error:
        print(f"Ошибка записи файла {filename}: {error}")


def load_users(filename: str) -> list[User]:
    path = Path(filename)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return [User.from_data(item) for item in data]
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"Ошибка чтения файла {filename}: {error}")
        return []


def save_users(filename: str, users: list[User]) -> None:
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [
                    {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                    }
                    for user in users
                ],
                file,
                ensure_ascii=False,
                indent=2,
            )
    except OSError as error:
        print(f"Ошибка записи файла {filename}: {error}")


def load_bookings(
    filename: str,
    tables: list[Table],
    users: list[User],
) -> list[Booking]:
    path = Path(filename)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, TypeError) as error:
        print(f"Ошибка чтения файла {filename}: {error}")
        return []

    bookings = []
    for item in data:
        table = find_table_by_number(tables, item["table_number"])
        user = find_user_by_id(users, item["user_id"])
        if table is None or user is None:
            print(
                f"Пропущено бронирование #{item.get('id')}: "
                f"связанный столик или пользователь не найден"
            )
            continue

        booking = Booking(
            booking_id=item["id"],
            table=table,
            booking_date=item["booking_date"],
            user=user,
        )
        booking.is_cancelled = item.get("is_cancelled", False)
        bookings.append(booking)

    return bookings


def save_bookings(filename: str, bookings: list[Booking]) -> None:
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [
                    {
                        "id": booking.id,
                        "table_number": booking.table.number,
                        "booking_date": booking.booking_date,
                        "user_id": booking.user.id,
                        "is_cancelled": booking.is_cancelled,
                    }
                    for booking in bookings
                ],
                file,
                ensure_ascii=False,
                indent=2,
            )
    except OSError as error:
        print(f"Ошибка записи файла {filename}: {error}")
