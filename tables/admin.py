from django.contrib import admin

from .models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "slug", "capacity", "location")
    list_filter = ("capacity",)
    search_fields = ("location", "slug")
    readonly_fields = ("slug",)
    ordering = ("number",)
