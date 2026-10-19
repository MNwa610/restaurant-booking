import json

from db.database import get_connection

TABLES_FILE = "data/tables.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_tables(conn):
    tables = load_json(TABLES_FILE)
    conn.executemany(
        """
        INSERT INTO tables (
            number,
            capacity,
            location
        )
        VALUES (?, ?, ?)
        """,
        [
            (
                table["number"],
                table["capacity"],
                table["location"],
            )
            for table in tables
        ],
    )


def import_users(conn):
    users = load_json(USERS_FILE)
    conn.executemany(
        """
        INSERT INTO users (
            id,
            name,
            email
        )
        VALUES (?, ?, ?)
        """,
        [
            (
                user["id"],
                user["name"],
                user["email"],
            )
            for user in users
        ],
    )


def import_bookings(conn):
    bookings = load_json(BOOKINGS_FILE)
    conn.executemany(
        """
        INSERT INTO bookings (
            id,
            table_number,
            user_id,
            booking_date,
            is_cancelled
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                booking["id"],
                booking["table_number"],
                booking["user_id"],
                booking["booking_date"],
                int(booking["is_cancelled"]),
            )
            for booking in bookings
        ],
    )


def main():
    conn = get_connection()
    try:
        import_tables(conn)
        import_users(conn)
        import_bookings(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
