# Generated by Django 5.0.3 on 2024-03-12 02:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("issue", "0001_initial"),
        ("voter", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VoterIssue",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "weight",
                    models.DecimalField(decimal_places=10, default=0.0, max_digits=10),
                ),
                (
                    "issue",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="issue.issue"
                    ),
                ),
                (
                    "voter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="voter.voter"
                    ),
                ),
            ],
        ),
    ]