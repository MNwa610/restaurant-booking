from django.conf import settings
from django.utils import timezone

from bookings.models import Booking


def restaurant_info(request):
    active_bookings_count = (
        Booking.objects.active().for_date(timezone.localdate()).count()
    )
    return {
        "restaurant_name": settings.RESTAURANT_NAME,
        "active_bookings_count": active_bookings_count,
    }
