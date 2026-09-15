from tables import add_table, find_table, check_capacity, sort_tables


def test_add_table():
    tables = {}
    add_table(tables, 1, 4, "У окна")
    assert len(tables) == 1
    assert tables[1]["capacity"] == 4


def test_find_table():
    tables = {}
    add_table(tables, 1, 4, "У окна")
    add_table(tables, 2, 6, "В центре зала")
    assert len(find_table(tables, "окна")) == 1
    assert len(find_table(tables, "центр")) == 1


def test_check_capacity_true():
    tables = {}
    add_table(tables, 1, 4, "У окна")
    assert check_capacity(tables, 1, 3) is True


def test_check_capacity_false():
    tables = {}
    add_table(tables, 1, 2, "У окна")
    assert check_capacity(tables, 1, 5) is False


def test_sort_tables():
    tables = {}
    add_table(tables, 1, 8, "Кабинет")
    add_table(tables, 2, 2, "У окна")
    add_table(tables, 3, 4, "Центр")
    sorted_tables = sort_tables(tables)
    assert sorted_tables[0]["capacity"] == 2
    assert sorted_tables[-1]["capacity"] == 8
