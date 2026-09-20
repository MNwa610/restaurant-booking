from models import Table
from models.tables import (
    add_table,
    check_capacity,
    find_table,
    find_table_by_number,
    sort_tables,
)


def test_table_creation():
    table = Table(1, 4, "У окна")
    assert table.number == 1
    assert table.capacity == 4
    assert table.location == "У окна"


def test_table_is_suitable_for():
    table = Table(1, 4, "У окна")
    assert table.is_suitable_for(3)
    assert not table.is_suitable_for(5)


def test_table_str():
    table = Table(1, 4, "У окна")
    assert "N1" in str(table)
    assert "4" in str(table)


def test_validate_capacity():
    assert Table.validate_capacity(4)
    assert not Table.validate_capacity(0)
    assert not Table.validate_capacity(25)


def test_add_table():
    tables = []
    add_table(tables, 1, 4, "У окна")
    assert len(tables) == 1
    assert isinstance(tables[0], Table)


def test_find_table_by_number():
    tables = []
    add_table(tables, 1, 4, "У окна")
    add_table(tables, 2, 6, "В центре зала")
    table = find_table_by_number(tables, 2)
    assert table is not None
    assert table.capacity == 6


def test_find_table():
    tables = []
    add_table(tables, 1, 4, "У окна")
    add_table(tables, 2, 6, "В центре зала")
    assert len(find_table(tables, "окна")) == 1
    assert len(find_table(tables, "центр")) == 1


def test_check_capacity():
    tables = []
    add_table(tables, 1, 4, "У окна")
    assert check_capacity(tables, 1, 3)
    assert not check_capacity(tables, 1, 5)


def test_sort_tables():
    tables = []
    add_table(tables, 1, 8, "Кабинет")
    add_table(tables, 2, 2, "У окна")
    add_table(tables, 3, 4, "Центр")
    sorted_tables = sort_tables(tables)
    assert sorted_tables[0].capacity == 2
    assert sorted_tables[-1].capacity == 8
