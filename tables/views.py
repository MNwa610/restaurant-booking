from datetime import date

from django.http import HttpResponse

from homepage.views import page
from models.bookings import is_table_available
from models.tables import find_table_by_number
from storage import load_bookings, load_tables, load_users


def tables(request):
    items = ""
    for table in load_tables("data/tables.json"):
        text = (
            f"Столик N{table.number} – "
            f"{table.capacity} мест ({table.location})"
        )
        items += (
            f'<li class="list-group-item">'
            f'<a href="/tables/{table.number}/">{text}</a>'
            f"</li>"
        )
    content = f"""
<h1>Столики</h1>
<ul class="list-group">{items}</ul>
"""
    return HttpResponse(page("Столики", content))


def table_detail(request, table_number):
    tables_list = load_tables("data/tables.json")
    table = find_table_by_number(tables_list, table_number)
    if table is None:
        content = """
<h1 class="text-danger">Столик не найден</h1>
<a href="/tables/" class="btn btn-outline-secondary">
← к списку столиков
</a>
"""
        return HttpResponse(
            page("Столик не найден", content),
            status=404,
        )

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
    status = "доступен" if available else "занят"
    badge = "bg-success" if available else "bg-danger"
    content = f"""
<div class="card">
<div class="card-body">
<h5 class="card-title">Столик N{table.number}</h5>
<p class="card-text">
<strong>Номер:</strong> {table.number}
</p>
<p class="card-text">
<strong>Вместимость:</strong> {table.capacity} мест
</p>
<p class="card-text">
<strong>Расположение:</strong> {table.location}
</p>
<p class="card-text">
Доступность на текущую дату:
<span class="badge {badge}">
{status}
</span>
</p>
<a href="/tables/"
class="btn btn-outline-secondary">
← к списку столиков
</a>
</div>
</div>
"""
    return HttpResponse(
        page(f"Столик N{table.number}", content),
        status=200,
    )
