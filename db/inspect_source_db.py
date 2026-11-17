import sqlite3
from pathlib import Path

SOURCE_DB = Path(__file__).resolve().parent.parent / "data" / (
    "restaurant_booking.sqlite"
)


def main():
    conn = sqlite3.connect(SOURCE_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    )
    tables = [row["name"] for row in cursor.fetchall()]
    print(f"База: {SOURCE_DB}")
    print(f"Таблицы: {tables}")
    for table_name in tables:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"\n{table_name}:")
        for column in columns:
            print(
                f"  {column['name']} {column['type']} "
                f"pk={column['pk']}"
            )
        cursor.execute(f"SELECT COUNT(*) AS cnt FROM {table_name}")
        count = cursor.fetchone()["cnt"]
        print(f"  количество строк: {count}")
    conn.close()


if __name__ == "__main__":
    main()
