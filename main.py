from datetime import date, time, datetime

# Данные клиента
client_name = "Цепляев Михаил"
client_phone = "+7-910-624-33-73"
client_email = "michael.tseplyaev@yandex.ru"

# Данные столика
table_number = 7
table_capacity = 4
table_location = "У окна"

# Данные бронирования
booking_date = date(2026, 9, 20)
booking_time = time(19, 0)
persons_count = 3

# Статус
is_booking_confirmed = False
booking_status = "Ожидает подтверждения"

# Проверка вместимости
is_capacity_enough = persons_count <= table_capacity

# Проверка времени (минимум 2 часа до брони)
current_datetime = datetime.now()
booking_datetime = datetime.combine(booking_date, booking_time)
hours_until_booking = (booking_datetime - current_datetime).total_seconds() / 3600
is_time_valid = hours_until_booking >= 2

# Проверка даты
is_date_valid = booking_date >= date.today()

# Проверка доступности (имитация)
is_table_available = True

# Основная логика
can_book = (is_capacity_enough and
            is_time_valid and
            is_date_valid and
            is_table_available)

if can_book:
    booking_status = "Подтверждено"
    is_booking_confirmed = True
    status_message = "Бронирование успешно создано!"
    confirmation_code = f"BK{table_number}{booking_date.day}{booking_time.hour}"
else:
    booking_status = "Отклонено"
    status_message = "Бронирование невозможно"
    confirmation_code = "НЕ СОЗДАН"

    rejection_reasons = []
    if not is_capacity_enough:
        rejection_reasons.append(f"Столик рассчитан на {table_capacity} человек, а требуется {persons_count}")
    if not is_time_valid:
        rejection_reasons.append(f"До бронирования осталось {int(hours_until_booking)} часов. Требуется минимум 2 часа")
    if not is_date_valid:
        rejection_reasons.append("Дата бронирования не может быть раньше сегодняшнего дня")
    if not is_table_available:
        rejection_reasons.append("Столик уже забронирован на это время")

# Вывод информации
print("=" * 60)
print("        СИСТЕМА БРОНИРОВАНИЯ СТОЛИКОВ")
print("=" * 60)
print()

print("ИНФОРМАЦИЯ О БРОНИРОВАНИИ")
print("-" * 40)
print(f"Клиент:          {client_name}")
print(f"Телефон:         {client_phone}")
print(f"Email:           {client_email}")
print()
print(f"Столик:          N{table_number}")
print(f"Вместимость:     {table_capacity} человек")
print(f"Расположение:    {table_location}")
print()
print(f"Дата:            {booking_date.strftime('%d.%m.%Y')}")
print(f"Время:           {booking_time.strftime('%H:%M')}")
print(f"Количество персон: {persons_count}")
print()

print("ПРОВЕРКА УСЛОВИЙ")
print("-" * 40)
print(f"  Вместимость достаточна:    {'ДА' if is_capacity_enough else 'НЕТ'}")
print(f"  Минимум 2 часа до брони:   {'ДА' if is_time_valid else 'НЕТ'}")
print(f"  Дата не раньше сегодня:    {'ДА' if is_date_valid else 'НЕТ'}")
print(f"  Столик свободен:           {'ДА' if is_table_available else 'НЕТ'}")
print()

print("РЕЗУЛЬТАТ")
print("-" * 40)
print(f"Статус:          {booking_status}")
print(f"Код бронирования: {confirmation_code}")
print()
print(f"{status_message}")
print()

if not can_book and rejection_reasons:
    print("ПРИЧИНЫ ОТКАЗА:")
    print("-" * 40)
    for reason in rejection_reasons:
        print(f"  - {reason}")

print()
print("=" * 60)

# Отмена бронирования
if is_booking_confirmed:
    print()
    print("ОТМЕНА БРОНИРОВАНИЯ")
    print("-" * 40)

    user_confirmation = "да"  # Имитация ввода
    if user_confirmation.lower() in ["да", "yes", "y", "+"]:
        booking_status = "Отменено"
        is_booking_confirmed = False
        print("Бронирование успешно отменено")
    else:
        print("Бронирование остаётся активным")

    print(f"Текущий статус: {booking_status}")