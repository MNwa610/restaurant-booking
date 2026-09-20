from datetime import datetime


def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_date(prompt: str) -> str:
    while True:
        try:
            value = input(prompt)
            parsed = datetime.strptime(value, "%d.%m.%Y").date()
            return parsed.isoformat()
        except ValueError:
            print("Ошибка: неверный формат даты. Используйте ДД.ММ.ГГГГ.")


def input_str(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: поле не может быть пустым.")
