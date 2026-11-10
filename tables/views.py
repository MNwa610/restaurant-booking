from datetime import date

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from tables.models import Table

TABLES_PER_PAGE = 2

TABLE_SORT_FIELDS = {
    "number": "number",
    "capacity": "capacity",
    "location": "location",
}


def parse_date(value):
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def tables(request):
    queryset = Table.objects.all()
    location = request.GET.get("location", "").strip()
    query = request.GET.get("q", "").strip()
    capacity = request.GET.get("capacity", "").strip()
    sort = request.GET.get("sort", "number")

    if location:
        queryset = queryset.filter(location__iexact=location)
    if query:
        queryset = queryset.filter(location__icontains=query)
    if capacity.isdigit():
        queryset = queryset.filter(capacity__gte=int(capacity))

    order_by = TABLE_SORT_FIELDS.get(sort, "number")
    queryset = queryset.order_by(order_by, "number")

    locations = (
        Table.objects.order_by("location")
        .values_list("location", flat=True)
        .distinct()
    )
    paginator = Paginator(queryset, TABLES_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "tables/table_list.html",
        {
            "tables": page_obj,
            "page_obj": page_obj,
            "locations": locations,
            "location": location,
            "q": query,
            "capacity": capacity,
            "sort": sort,
        },
    )


def table_detail(request, table_number):
    table = get_object_or_404(Table, pk=table_number)
    today = date.today()
    available = (
        Table.objects.filter(pk=table.number)
        .exclude(
            bookings__booking_date=today,
            bookings__is_cancelled=False,
        )
        .exists()
    )
    return render(
        request,
        "tables/table_detail.html",
        {
            "table": table,
            "available": available,
        },
    )


def available_tables(request):
    date_input = request.GET.get("date", "").strip()
    booking_date = parse_date(date_input)
    date_error = bool(date_input) and booking_date is None
    tables_list = Table.objects.none()
    if booking_date:
        tables_list = (
            Table.objects.exclude(
                bookings__booking_date=booking_date,
                bookings__is_cancelled=False,
            )
            .distinct()
            .order_by("number")
        )
    return render(
        request,
        "tables/available.html",
        {
            "tables": tables_list,
            "booking_date": date_input if booking_date else date_input,
            "date_error": date_error,
        },
    )
