from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import connection
from django.db.models import ProtectedError
from django.db.migrations.executor import MigrationExecutor
from django.urls import reverse

from bookings.admin import cancel_selected_bookings
from bookings.models import Booking, BookingStatus, User
from tables.models import Table

DAY = date(2026, 9, 20)
OTHER_DAY = date(2026, 9, 21)


def make_table(number=7, location="У окна"):
    return Table.objects.create(
        number=number,
        capacity=4,
        location=location,
    )


def make_user(email="ivan@example.com"):
    return User.objects.create(name="Иван", email=email)


def make_booking(table, user, booking_date=DAY, status=BookingStatus.ACTIVE):
    return Booking.objects.create(
        table=table,
        user=user,
        booking_date=booking_date,
        status=status,
    )


@pytest.mark.django_db
def test_booking_status_choices_and_default():
    booking = make_booking(make_table(), make_user())
    assert BookingStatus.ACTIVE == "active"
    assert BookingStatus.ACTIVE.label == "Активно"
    assert BookingStatus.CANCELLED.label == "Отменено"
    assert BookingStatus.COMPLETED.label == "Завершено"
    assert booking.status == BookingStatus.ACTIVE
    assert "Активно" in str(booking)
    booking.status = BookingStatus.CANCELLED
    booking.save(update_fields=["status"])
    assert "Отменено" in str(booking)


@pytest.mark.django_db
def test_queryset_active_and_cancelled():
    table = make_table()
    user = make_user()
    active = make_booking(table, user, DAY, BookingStatus.ACTIVE)
    cancelled = make_booking(
        table,
        user,
        OTHER_DAY,
        BookingStatus.CANCELLED,
    )
    make_booking(
        make_table(8, "Терраса"),
        user,
        DAY,
        BookingStatus.COMPLETED,
    )
    assert set(Booking.objects.active()) == {active}
    assert set(Booking.objects.cancelled()) == {cancelled}


@pytest.mark.django_db
def test_queryset_for_date():
    table = make_table()
    user = make_user()
    on_day = make_booking(table, user, DAY)
    make_booking(table, user, OTHER_DAY)
    assert list(Booking.objects.for_date(DAY)) == [on_day]


@pytest.mark.django_db
def test_queryset_occupied_on_ignores_cancelled():
    table = make_table()
    other = make_table(8, "Терраса")
    free = make_table(9, "Кабинет")
    user = make_user()
    make_booking(table, user, DAY, BookingStatus.ACTIVE)
    make_booking(other, user, DAY, BookingStatus.COMPLETED)
    make_booking(free, user, DAY, BookingStatus.CANCELLED)
    make_booking(free, user, OTHER_DAY, BookingStatus.ACTIVE)
    occupied = {
        row["table_id"]
        for row in Booking.objects.occupied_on(DAY)
    }
    assert occupied == {table.number, other.number}


@pytest.mark.django_db
def test_table_slug_and_absolute_url(client):
    table = make_table()
    assert table.slug == "table-7"
    assert table.get_absolute_url() == reverse(
        "tables:detail",
        kwargs={"slug": "table-7"},
    )
    response = client.get(table.get_absolute_url())
    assert response.status_code == 200
    assert "Столик N7" in response.content.decode()
    missing = client.get(reverse("tables:detail", kwargs={"slug": "missing"}))
    assert missing.status_code == 404
    legacy = client.get(reverse("tables:detail_legacy", args=[table.number]))
    assert legacy.status_code == 302
    assert legacy.url == table.get_absolute_url()


@pytest.mark.django_db
def test_cancel_bookings_admin_action():
    booking = make_booking(make_table(), make_user())
    cancel_selected_bookings(
        None,
        None,
        Booking.objects.filter(pk=booking.pk),
    )
    booking.refresh_from_db()
    assert booking.status == BookingStatus.CANCELLED


@pytest.mark.django_db
def test_admin_cancel_action_from_changelist(client):
    admin_user = get_user_model().objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="pass",
    )
    client.force_login(admin_user)
    booking = make_booking(make_table(), make_user())
    response = client.post(
        reverse("admin:bookings_booking_changelist"),
        {
            "action": "cancel_selected_bookings",
            "_selected_action": [str(booking.pk)],
        },
        follow=True,
    )
    assert response.status_code == 200
    booking.refresh_from_db()
    assert booking.status == BookingStatus.CANCELLED


@pytest.mark.django_db
def test_protected_table_delete_shows_error(client):
    admin_user = get_user_model().objects.create_superuser(
        username="admin2",
        email="admin2@example.com",
        password="pass",
    )
    client.force_login(admin_user)
    table = make_table()
    make_booking(table, make_user())
    with pytest.raises(ProtectedError):
        table.delete()
    url = reverse("admin:tables_table_delete", args=[table.number])
    response = client.post(url, {"post": "yes"})
    assert response.status_code == 200
    page = response.content.decode()
    assert "защищ" in page.lower()
    assert Table.objects.filter(pk=table.number).exists()


@pytest.mark.django_db(transaction=True)
def test_status_data_migration_and_reverse():
    executor = MigrationExecutor(connection)
    old_state = [
        ("tables", "0001_initial"),
        ("bookings", "0002_add_booking_status"),
    ]
    new_state = [
        ("tables", "0002_add_table_slug"),
        ("bookings", "0004_replace_cancelled_flag"),
    ]
    try:
        executor.migrate(old_state)
        apps = executor.loader.project_state(old_state).apps
        HistoricalTable = apps.get_model("tables", "Table")
        HistoricalUser = apps.get_model("bookings", "User")
        HistoricalBooking = apps.get_model("bookings", "Booking")
        table = HistoricalTable.objects.create(
            number=41,
            capacity=2,
            location="Тест",
        )
        user = HistoricalUser.objects.create(
            name="Тест",
            email="status@example.com",
        )
        HistoricalBooking.objects.create(
            table=table,
            user=user,
            booking_date=DAY,
            is_cancelled=True,
        )
        HistoricalBooking.objects.create(
            table=table,
            user=user,
            booking_date=OTHER_DAY,
            is_cancelled=False,
        )

        executor = MigrationExecutor(connection)
        executor.migrate(new_state)
        BookingModel = executor.loader.project_state(new_state).apps.get_model(
            "bookings",
            "Booking",
        )
        cancelled = BookingModel.objects.get(booking_date=DAY)
        active = BookingModel.objects.get(booking_date=OTHER_DAY)
        assert cancelled.status == "cancelled"
        assert active.status == "active"
        names = {field.name for field in BookingModel._meta.fields}
        assert "is_cancelled" not in names
        assert active.booking_key == f"{OTHER_DAY.isoformat()}-41"

        executor = MigrationExecutor(connection)
        executor.migrate(old_state)
        BookingModel = executor.loader.project_state(old_state).apps.get_model(
            "bookings",
            "Booking",
        )
        cancelled = BookingModel.objects.get(booking_date=DAY)
        active = BookingModel.objects.get(booking_date=OTHER_DAY)
        assert cancelled.is_cancelled is True
        assert active.is_cancelled is False
    finally:
        call_command("migrate", verbosity=0)
        Booking.objects.filter(user__email="status@example.com").delete()
        User.objects.filter(email="status@example.com").delete()
        Table.objects.filter(number=41).delete()
