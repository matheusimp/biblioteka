# Generated by Django 4.2 on 2023-04-30 22:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("biblioteka", "0004_alter_borrower_options_alter_countrystate_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "inventory_id",
                    models.CharField(unique=True, verbose_name="ID do estoque"),
                ),
                ("isbn", models.CharField(max_length=13, verbose_name="ISBN")),
                (
                    "available",
                    models.BooleanField(default=True, verbose_name="disponível"),
                ),
                ("title", models.CharField(max_length=255, verbose_name="título")),
                (
                    "subtitle",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        verbose_name="subtítulo",
                    ),
                ),
                (
                    "author",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        verbose_name="autor",
                    ),
                ),
                (
                    "genre",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        verbose_name="gênero",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        default=None,
                        max_length=1000,
                        null=True,
                        verbose_name="descrição",
                    ),
                ),
                (
                    "pages",
                    models.IntegerField(
                        blank=True, default=None, null=True, verbose_name="páginas"
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=100,
                        null=True,
                        verbose_name="idioma",
                    ),
                ),
                (
                    "publisher",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        verbose_name="editora",
                    ),
                ),
                (
                    "publication_date",
                    models.DateField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="data de publicação",
                    ),
                ),
            ],
            options={
                "verbose_name": "livro",
            },
        ),
    ]