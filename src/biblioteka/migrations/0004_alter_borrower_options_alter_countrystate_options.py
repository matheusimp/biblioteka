# Generated by Django 4.2 on 2023-04-16 03:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("biblioteka", "0003_borrower"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="borrower",
            options={"verbose_name": "cliente"},
        ),
        migrations.AlterModelOptions(
            name="countrystate",
            options={"verbose_name": "estado"},
        ),
    ]