from typing import Optional


class Table:
    def __init__(
        self,
        table_number: int,
        capacity: int,
        location: str,
    ) -> None:
        self.number = table_number
        self.capacity = capacity
        self.location = location

    def is_suitable_for(self, persons_count: int) -> bool:
        return self.capacity >= persons_count

    @staticmethod
    def validate_capacity(capacity: int) -> bool:
        return 1 <= capacity <= 20

    def __str__(self) -> str:
        return (
            f"Столик N{self.number} "
            f"({self.capacity} мест, {self.location})"
        )


def add_table(
    tables: list[Table],
    table_number: int,
    capacity: int,
    location: str,
) -> Table:
    table = Table(table_number, capacity, location)
    tables.append(table)
    return table


def find_table_by_number(
    tables: list[Table], number: int
) -> Optional[Table]:
    for table in tables:
        if table.number == number:
            return table
    return None


def find_table(
    tables: list[Table], query: str
) -> list[Table]:
    query_lower = query.lower()
    return [
        table
        for table in tables
        if query_lower in table.location.lower()
    ]


def check_capacity(
    tables: list[Table], number: int, min_capacity: int
) -> bool:
    table = find_table_by_number(tables, number)
    return table is not None and table.is_suitable_for(min_capacity)


def filter_by_capacity(
    tables: list[Table], min_capacity: int
) -> list[Table]:
    return [
        table
        for table in tables
        if table.is_suitable_for(min_capacity)
    ]


def sort_tables(tables: list[Table]) -> list[Table]:
    return sorted(tables, key=lambda table: table.capacity)


def show_tables(tables: list[Table]) -> None:
    if not tables:
        print("Список столиков пуст.")
        return

    print("\nСтолики ресторана:")
    print("-" * 50)
    for table in sort_tables(tables):
        print(f"  {table}")
    print("-" * 50)
