from typing import Optional


class User:
    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id = user_id
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "User":
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


def add_user(
    users: list[User], user_id: int, name: str, email: str
) -> User:
    user = User(user_id, name, email)
    users.append(user)
    return user


def find_user_by_id(
    users: list[User], user_id: int
) -> Optional[User]:
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_user(users: list[User], query: str) -> list[User]:
    query_lower = query.lower()
    return [
        user
        for user in users
        if query_lower in user.name.lower()
        or query_lower in user.email.lower()
    ]


def show_users(users: list[User]) -> None:
    if not users:
        print("Список пользователей пуст.")
        return

    print("\nПользователи:")
    print("-" * 50)
    for user in users:
        print(f"  N{user.id}: {user}")
    print("-" * 50)
