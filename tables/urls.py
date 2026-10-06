from django.urls import path

from . import views

urlpatterns = [
    path("", views.tables, name="tables"),
    path("<int:table_number>/", views.table_detail, name="table_detail"),
]
