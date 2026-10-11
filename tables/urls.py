from django.urls import path

from . import views

app_name = "tables"

urlpatterns = [
    path("", views.tables, name="list"),
    path("<int:table_number>/", views.table_detail, name="detail"),
]
