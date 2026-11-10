from django.db import models

from tables.models import Table, TimeStampedModel


class User(TimeStampedModel):
    name = models.CharField(
        max_length=150,
        verbose_name="Имя",
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Booking(TimeStampedModel):
    table = models.ForeignKey(
        Table,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Столик",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Пользователь",
    )
    booking_date = models.DateField(
        verbose_name="Дата бронирования",
    )
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name="Отменено",
    )

    class Meta:
        ordering = ["booking_date", "id"]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        status = "Отменено" if self.is_cancelled else "Активно"
        return (
            f"Бронирование #{self.id} | "
            f"{self.table} | "
            f"{self.booking_date} | "
            f"{self.user.name} | "
            f"{status}"
        )

    @property
    def table_number(self):
        return self.table.number

    @property
    def capacity(self):
        return self.table.capacity

    @property
    def user_name(self):
        return self.user.name
