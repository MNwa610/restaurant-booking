from django.db import models
from django.db.models import CharField, Value
from django.db.models.functions import Cast, Concat

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


class BookingStatus(models.TextChoices):
    ACTIVE = "active", "Активно"
    CANCELLED = "cancelled", "Отменено"
    COMPLETED = "completed", "Завершено"


class BookingQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=BookingStatus.ACTIVE)

    def cancelled(self):
        return self.filter(status=BookingStatus.CANCELLED)

    def for_date(self, booking_date):
        return self.filter(booking_date=booking_date)

    def occupied_on(self, booking_date):
        return self.filter(
            booking_date=booking_date,
            status__in=(
                BookingStatus.ACTIVE,
                BookingStatus.COMPLETED,
            ),
        ).values("table_id")


class BookingManager(models.Manager):
    def get_queryset(self):
        return BookingQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def cancelled(self):
        return self.get_queryset().cancelled()

    def for_date(self, booking_date):
        return self.get_queryset().for_date(booking_date)

    def occupied_on(self, booking_date):
        return self.get_queryset().occupied_on(booking_date)


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
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.ACTIVE,
        verbose_name="Статус",
    )
    booking_key = models.GeneratedField(
        expression=Concat(
            Cast("booking_date", output_field=CharField()),
            Value("-"),
            Cast("table_id", output_field=CharField()),
        ),
        output_field=CharField(max_length=40),
        db_persist=True,
    )

    objects = BookingManager()

    class Meta:
        ordering = ["booking_date", "id"]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return (
            f"Бронирование #{self.id} | "
            f"{self.table} | "
            f"{self.booking_date} | "
            f"{self.user.name} | "
            f"{self.get_status_display()}"
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
