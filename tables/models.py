from django.db import models
from django.urls import reverse
from django.utils.text import slugify


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
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True,
        verbose_name="Слаг",
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._build_slug()
        super().save(*args, **kwargs)

    def _build_slug(self):
        located = slugify(f"{self.location}-{self.number}")
        if located and not located.isdigit():
            return located
        return f"table-{self.number}"

    def get_absolute_url(self):
        return reverse("tables:detail", kwargs={"slug": self.slug})
