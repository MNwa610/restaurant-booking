from tables import (
    add_table,
    find_table,
    check_capacity,
    sort_tables,
)
from bookings import (
    is_table_available,
    create_booking,
    cancel_booking,
    get_booking_status,
)
from storage import (
    load_tables,
    save_tables,
    load_bookings,
    save_bookings,
)
from utils import input_int, input_date, input_str

TABLES_FILE = "data/tables.json"
BOOKINGS_FILE = "data/bookings.json"


def show_tables(tables: dict[int, dict]) -> None:
    """Вывести список столиков."""
    if not tables:
        print("Список столиков пуст.")
        return

    print("\nСтолики ресторана:")
    print("-" * 50)
    for table in sort_tables(tables):
        print(
            f"  N{table['number']:>3} | "
            f"{table['capacity']} мест | {table['location']}"
        )
    print("-" * 50)


def show_bookings(bookings: list[dict]) -> None:
    """Вывести список бронирований."""
    if not bookings:
        print("Бронирований пока нет.")
        return

    print("\nБронирования:")
    print("-" * 70)
    for booking in bookings:
        print(
            f"  #{booking['id']:<3} | "
            f"Столик N{booking['table_number']:<3} | "
            f"{booking['date']} | "
            f"{booking['client_name']:<20} | "
            f"{booking['status']}"
        )
    print("-" * 70)


def menu() -> None:
    """Главное меню приложения."""
    print("\n" + "=" * 60)
    print("        СИСТЕМА БРОНИРОВАНИЯ СТОЛИКОВ")
    print("=" * 60)
    print("1. Показать столики")
    print("2. Найти столик по расположению")
    print("3. Проверить вместимость столика")
    print("4. Проверить доступность на дату")
    print("5. Забронировать столик")
    print("6. Отменить бронирование")
    print("7. Показать бронирования")
    print("0. Выход")


def main() -> None:
    """Запуск приложения."""
    tables = load_tables(TABLES_FILE)
    bookings = load_bookings(BOOKINGS_FILE)

    # Если данных ещё нет — добавляем стартовые столики
    if not tables:
        add_table(tables, 1, 2, "У окна")
        add_table(tables, 2, 4, "В центре зала")
        add_table(tables, 3, 4, "У окна")
        add_table(tables, 4, 6, "В центре зала")
        add_table(tables, 5, 8, "Отдельный кабинет")
        save_tables(TABLES_FILE, tables)

    while True:
        menu()
        choice = input_int("\nВыберите действие: ")

        if choice == 0:
            save_tables(TABLES_FILE, tables)
            save_bookings(BOOKINGS_FILE, bookings)
            print("Данные сохранены. До свидания!")
            break

        if choice == 1:
            show_tables(tables)

        elif choice == 2:
            query = input_str("Подстрока расположения: ")
            found = find_table(tables, query)
            if found:
                for table in found:
                    print(
                        f"  N{table['number']} | "
                        f"{table['capacity']} мест | "
                        f"{table['location']}"
                    )
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
            number = input_int("Номер столика: ")
            booking_date = input_date("Дата (ДД.ММ.ГГГГ): ")
            available = is_table_available(bookings, number, booking_date)
            print(get_booking_status(available))

        elif choice == 5:
            number = input_int("Номер столика: ")
            booking_date = input_date("Дата (ДД.ММ.ГГГГ): ")
            client_name = input_str("Имя клиента: ")
            booking = create_booking(
                bookings, number, booking_date, client_name
            )
            if booking:
                print(f"Бронирование #{booking['id']} успешно создано!")
                save_bookings(BOOKINGS_FILE, bookings)
            else:
                print("Столик уже забронирован на эту дату.")

        elif choice == 6:
            booking_id = input_int("Номер бронирования: ")
            if cancel_booking(bookings, booking_id):
                print("Бронирование отменено.")
                save_bookings(BOOKINGS_FILE, bookings)
            else:
                print("Бронирование не найдено или уже отменено.")

        elif choice == 7:
            show_bookings(bookings)

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
