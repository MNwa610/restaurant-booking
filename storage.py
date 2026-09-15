import json
from pathlib import Path


def load_tables(filename: str) -> dict[int, dict]:
    path = Path(filename)
    if not path.exists():
        return {}

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return {int(item["number"]): item for item in data}
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"Ошибка чтения файла {filename}: {error}")
        return {}


def save_tables(filename: str, tables: dict[int, dict]) -> None:
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                list(tables.values()),
                file,
                ensure_ascii=False,
                indent=2,
            )
    except OSError as error:
        print(f"Ошибка записи файла {filename}: {error}")


def load_bookings(filename: str) -> list[dict]:
    path = Path(filename)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, TypeError) as error:
        print(f"Ошибка чтения файла {filename}: {error}")
        return []


def save_bookings(filename: str, bookings: list[dict]) -> None:
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(bookings, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка записи файла {filename}: {error}")
