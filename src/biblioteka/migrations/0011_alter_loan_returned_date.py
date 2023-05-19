# Generated by Django 4.2 on 2023-05-18 23:08

from django.db import migrations, models

import biblioteka.models


class Migration(migrations.Migration):
    dependencies = [
        ("biblioteka", "0010_populate_loan_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="returned_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[biblioteka.models.validate_date_not_in_future],
                verbose_name="data de devolução",
            ),
        ),
    ]
