from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Min, Q, Sum
from django.shortcuts import get_object_or_404, render

from bookings.models import Booking, BookingStatus, User
from tables.models import Table
from tables.views import parse_date

BOOKINGS_PER_PAGE = 2

BOOKING_SORT_FIELDS = {
    "date": "booking_date",
    "table": "table__number",
    "user": "user__name",
    "-date": "-booking_date",
    "-table": "-table__number",
    "-user": "-user__name",
}


def bookings(request):
    queryset = Booking.objects.select_related("table", "user")
    date_input = request.GET.get("date", "").strip()
    booking_date = parse_date(date_input)
    date_error = bool(date_input) and booking_date is None
    table_number = request.GET.get("table", "").strip()
    user_id = request.GET.get("user", "").strip()
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "active")
    sort = request.GET.get("sort", "date")

    if booking_date:
        queryset = queryset.for_date(booking_date)
    if table_number.isdigit():
        queryset = queryset.filter(table__number=int(table_number))

    if user_id.isdigit():
        try:
            selected_user = User.objects.get(pk=int(user_id))
        except User.DoesNotExist:
            selected_user = None
        else:
            queryset = queryset.filter(user=selected_user)

    if query:
        queryset = queryset.filter(
            Q(user__name__istartswith=query)
            | Q(user__email__icontains=query)
            | Q(table__location__icontains=query)
        )

    if status == "cancelled":
        queryset = queryset.cancelled()
    elif status == "completed":
        queryset = queryset.filter(status=BookingStatus.COMPLETED)
    elif status != "all":
        queryset = queryset.active()

    order_by = BOOKING_SORT_FIELDS.get(sort, "booking_date")
    queryset = queryset.order_by(order_by, "table__number", "id")
    queryset = queryset.annotate(
        annotated_table_number=F("table__number"),
        annotated_user_name=F("user__name"),
        annotated_capacity=F("table__capacity"),
    )

    paginator = Paginator(queryset, BOOKINGS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "bookings/booking_list.html",
        {
            "bookings": page_obj,
            "page_obj": page_obj,
            "tables": Table.objects.all(),
            "users": User.objects.order_by("name").values("id", "name"),
            "date": date_input,
            "table": table_number,
            "user": user_id,
            "q": query,
            "status": status,
            "sort": sort,
            "date_error": date_error,
        },
    )


def booking_detail(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("table", "user"),
        pk=booking_id,
    )
    return render(
        request,
        "bookings/booking_detail.html",
        {"booking": booking},
    )


def statistics(request):
    statistics_data = (
        Table.objects.annotate(
            table_number=F("number"),
            bookings_count=Count(
                "bookings",
                filter=Q(
                    bookings__status__in=(
                        BookingStatus.ACTIVE,
                        BookingStatus.COMPLETED,
                    )
                ),
            ),
        ).order_by("-bookings_count", "number")
    )
    summary = Booking.objects.aggregate(
        total=Count("id"),
        cancelled=Count("id", filter=Q(status=BookingStatus.CANCELLED)),
    )
    status_counts = list(
        Booking.objects.values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )
    status_labels = dict(BookingStatus.choices)
    for row in status_counts:
        row["label"] = status_labels.get(row["status"], row["status"])
    capacity_stats = Table.objects.aggregate(
        avg_capacity=Avg("capacity"),
        min_capacity=Min("capacity"),
        max_capacity=Max("capacity"),
        sum_capacity=Sum("capacity"),
        tables_count=Count("number"),
    )
    locations = (
        Table.objects.values("location")
        .annotate(tables_count=Count("number"))
        .order_by("-tables_count", "location")
    )
    return render(
        request,
        "bookings/statistics.html",
        {
            "statistics": statistics_data,
            "summary": summary,
            "status_counts": status_counts,
            "capacity_stats": capacity_stats,
            "locations": locations,
        },
    )
