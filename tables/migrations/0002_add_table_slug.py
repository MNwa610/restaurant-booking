from django.db import migrations, models


def fill_table_slugs(apps, schema_editor):
    Table = apps.get_model("tables", "Table")
    for table in Table.objects.all():
        base = f"table-{table.number}"
        slug = base
        suffix = 2
        while (
            Table.objects.filter(slug=slug)
            .exclude(pk=table.pk)
            .exists()
        ):
            slug = f"{base}-{suffix}"
            suffix += 1
        table.slug = slug
        table.save(update_fields=["slug"])


def clear_table_slugs(apps, schema_editor):
    Table = apps.get_model("tables", "Table")
    Table.objects.update(slug=None)


class Migration(migrations.Migration):

    dependencies = [
        ("tables", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="table",
            name="slug",
            field=models.SlugField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="Слаг",
            ),
        ),
        migrations.RunPython(fill_table_slugs, clear_table_slugs),
        migrations.AlterField(
            model_name="table",
            name="slug",
            field=models.SlugField(
                blank=True,
                max_length=50,
                unique=True,
                verbose_name="Слаг",
            ),
        ),
    ]
