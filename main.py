from models import Booking, Table, User
from models.tables import (
    add_table,
    check_capacity,
    find_table,
    find_table_by_number,
    show_tables,
)
from models.users import (
    add_user,
    find_user_by_id,
    show_users,
)
from models.bookings import (
    cancel_booking,
    create_booking,
    get_booking_status,
    is_table_available,
    show_bookings,
)
from storage import (
    load_bookings,
    load_tables,
    load_users,
    save_bookings,
    save_tables,
    save_users,
)
from utils import input_date, input_int, input_str

TABLES_FILE = "data/tables.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def menu() -> None:
    print("\n" + "=" * 60)
    print("        СИСТЕМА БРОНИРОВАНИЯ СТОЛИКОВ")
    print("=" * 60)
    print("1. Показать столики")
    print("2. Найти столик по расположению")
    print("3. Проверить вместимость столика")
    print("4. Показать пользователей")
    print("5. Проверить доступность на дату")
    print("6. Забронировать столик")
    print("7. Отменить бронирование")
    print("8. Показать бронирования")
    print("0. Выход")


def create_new_booking(
    bookings: list[Booking],
    tables: list[Table],
    users: list[User],
) -> None:
    table_number = input_int("Номер столика: ")
    table = find_table_by_number(tables, table_number)
    if table is None:
        print("Столик не найден.")
        return

    user_id = input_int("ID пользователя: ")
    user = find_user_by_id(users, user_id)
    if user is None:
        print("Пользователь не найден.")
        return

    booking_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    booking = create_booking(bookings, table, booking_date, user)

    if booking is None:
        print("Столик уже забронирован на эту дату.")
        return

    print(f"Бронирование #{booking.id} успешно создано!")


def main() -> None:
    tables = load_tables(TABLES_FILE)
    users = load_users(USERS_FILE)

    if not tables:
        add_table(tables, 1, 2, "У окна")
        add_table(tables, 2, 4, "В центре зала")
        add_table(tables, 3, 4, "У окна")
        add_table(tables, 4, 6, "В центре зала")
        add_table(tables, 5, 8, "Отдельный кабинет")
        save_tables(TABLES_FILE, tables)

    if not users:
        add_user(users, 1, "Иван Петров", "ivan@example.com")
        add_user(users, 2, "Мария Сидорова", "maria@example.com")
        save_users(USERS_FILE, users)

    bookings = load_bookings(BOOKINGS_FILE, tables, users)

    while True:
        menu()
        choice = input_int("\nВыберите действие: ")

        if choice == 0:
            save_tables(TABLES_FILE, tables)
            save_users(USERS_FILE, users)
            save_bookings(BOOKINGS_FILE, bookings)
            print("Данные сохранены. До свидания!")
            break

        elif choice == 1:
            show_tables(tables)

        elif choice == 2:
            query = input_str("Подстрока расположения: ")
            found = find_table(tables, query)
            if found:
                for table in found:
                    print(f"  {table}")
            else:
                print("Столики не найдены.")

        elif choice == 3:
            number = input_int("Номер столика: ")
            min_capacity = input_int("Минимальная вместимость: ")
            if check_capacity(tables, number, min_capacity):
                print("Вместимость достаточна.")
            else:
                print("Вместимость недостаточна.")

        elif choice == 4:
            show_users(users)

        elif choice == 5:
            number = input_int("Номер столика: ")
            table = find_table_by_number(tables, number)
            if table is None:
                print("Столик не найден.")
                continue
            booking_date = input_date("Дата (ДД.ММ.ГГГГ): ")
            available = is_table_available(bookings, table, booking_date)
            print(get_booking_status(available))

        elif choice == 6:
            create_new_booking(bookings, tables, users)
            save_bookings(BOOKINGS_FILE, bookings)

        elif choice == 7:
            booking_id = input_int("Номер бронирования: ")
            if cancel_booking(bookings, booking_id):
                print("Бронирование отменено.")
                save_bookings(BOOKINGS_FILE, bookings)
            else:
                print("Бронирование не найдено или уже отменено.")

        elif choice == 8:
            show_bookings(bookings)

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
