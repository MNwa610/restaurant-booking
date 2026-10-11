from datetime import date

from django.shortcuts import render

from models.bookings import is_table_available
from models.tables import find_table_by_number
from storage import load_bookings, load_tables, load_users


def tables(request):
    tables_list = load_tables("data/tables.json")
    context = {
        "tables": tables_list,
    }
    return render(
        request,
        "tables/table_list.html",
        context,
    )


def table_detail(request, table_number):
    tables_list = load_tables("data/tables.json")
    table = find_table_by_number(
        tables_list,
        table_number,
    )
    available = False
    if table is not None:
        users_list = load_users("data/users.json")
        bookings_list = load_bookings(
            "data/bookings.json",
            tables_list,
            users_list,
        )
        available = is_table_available(
            bookings_list,
            table,
            date.today().isoformat(),
        )
    context = {
        "table": table,
        "available": available,
    }
    return render(
        request,
        "tables/table_detail.html",
        context,
        status=404 if table is None else 200,
    )
