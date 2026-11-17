from django.db import migrations


def copy_is_cancelled_to_status(apps, schema_editor):
    Booking = apps.get_model("bookings", "Booking")
    Booking.objects.filter(is_cancelled=True).update(status="cancelled")
    Booking.objects.filter(is_cancelled=False).update(status="active")


def copy_status_to_is_cancelled(apps, schema_editor):
    Booking = apps.get_model("bookings", "Booking")
    Booking.objects.filter(status="cancelled").update(is_cancelled=True)
    Booking.objects.exclude(status="cancelled").update(is_cancelled=False)


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0002_add_booking_status"),
    ]

    operations = [
        migrations.RunPython(
            copy_is_cancelled_to_status,
            copy_status_to_is_cancelled,
        ),
    ]
