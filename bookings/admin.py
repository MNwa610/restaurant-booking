from django.contrib import admin

from .models import Booking, BookingStatus, User


@admin.action(description="Отменить выбранные бронирования")
def cancel_selected_bookings(modeladmin, request, queryset):
    queryset.update(status=BookingStatus.CANCELLED)


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
        "status",
    )
    list_filter = ("status", "booking_date")
    search_fields = ("table__location", "user__name", "user__email")
    ordering = ("booking_date",)
    actions = (cancel_selected_bookings,)
