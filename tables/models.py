from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлено",
    )

    class Meta:
        abstract = True


class Table(TimeStampedModel):
    number = models.PositiveIntegerField(
        primary_key=True,
        verbose_name="Номер",
    )
    capacity = models.PositiveIntegerField(
        verbose_name="Вместимость",
    )
    location = models.TextField(
        verbose_name="Расположение",
    )

    class Meta:
        ordering = ["number"]
        verbose_name = "Столик"
        verbose_name_plural = "Столики"

    def __str__(self):
        return (
            f"Столик N{self.number} "
            f"({self.capacity} мест, {self.location})"
        )
