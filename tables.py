def add_table(
    tables: dict[int, dict],
    number: int,
    capacity: int,
    location: str,
) -> None:
    tables[number] = {
        "number": number,
        "capacity": capacity,
        "location": location,
    }


def find_table(tables: dict[int, dict], query: str) -> list[dict]:
    query_lower = query.lower()
    return [
        table
        for table in tables.values()
        if query_lower in table["location"].lower()
    ]


def check_capacity(
    tables: dict[int, dict], number: int, min_capacity: int
) -> bool:
    table = tables.get(number)
    return table is not None and table["capacity"] >= min_capacity


def filter_by_capacity(
    tables: dict[int, dict], min_capacity: int
) -> list[dict]:
    return [
        table
        for table in tables.values()
        if table["capacity"] >= min_capacity
    ]


def sort_tables(tables: dict[int, dict]) -> list[dict]:
    return sorted(tables.values(), key=lambda t: t["capacity"])
