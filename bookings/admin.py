from django.contrib import admin

from .models import Booking, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    search_fields = ("name", "email")
    ordering = ("name",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "table",
        "user",
        "booking_date",
        "is_cancelled",
    )
    list_filter = ("is_cancelled", "booking_date")
    search_fields = ("user__name", "user__email")
    ordering = ("booking_date",)
