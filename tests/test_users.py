from models import User
from models.users import add_user, find_user, find_user_by_id


def test_user_creation():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert user.id == 1
    assert user.name == "Иван Петров"
    assert user.email == "ivan@example.com"


def test_user_str():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert "Иван Петров" in str(user)
    assert "ivan@example.com" in str(user)


def test_user_from_data():
    data = {"id": 5, "name": "Анна", "email": "anna@example.com"}
    user = User.from_data(data)
    assert user.id == 5
    assert user.name == "Анна"


def test_add_user():
    users = []
    add_user(users, 1, "Иван", "ivan@example.com")
    assert len(users) == 1
    assert isinstance(users[0], User)


def test_find_user_by_id():
    users = []
    add_user(users, 1, "Иван", "ivan@example.com")
    add_user(users, 2, "Мария", "maria@example.com")
    user = find_user_by_id(users, 2)
    assert user is not None
    assert user.name == "Мария"


def test_find_user_by_query():
    users = []
    add_user(users, 1, "Иван", "ivan@example.com")
    add_user(users, 2, "Мария", "maria@example.com")
    assert len(find_user(users, "иван")) == 1
    assert len(find_user(users, "maria")) == 1
