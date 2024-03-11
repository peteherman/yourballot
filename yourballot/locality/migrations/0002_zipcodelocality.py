# Generated by Django 5.0.3 on 2024-03-11 02:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locality", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ZipcodeLocality",
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
                ("zipcode", models.CharField(max_length=5)),
                (
                    "political_locality",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="locality.politicallocality",
                    ),
                ),
            ],
        ),
    ]