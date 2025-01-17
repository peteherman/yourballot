# Generated by Django 5.0.3 on 2024-03-12 01:54

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("voter", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Issue",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "external_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("name", models.CharField(max_length=250, unique=True)),
                (
                    "description",
                    models.CharField(blank=True, default="", max_length=1024),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[("SOCIAL", "Social"), ("ECONOMIC", "Economic")],
                        max_length=64,
                    ),
                ),
                (
                    "low_score_tendency",
                    models.CharField(
                        choices=[("LEFT", "Left"), ("RIGHT", "Right")], max_length=64
                    ),
                ),
                (
                    "high_score_tendency",
                    models.CharField(
                        choices=[("LEFT", "Left"), ("RIGHT", "Right")], max_length=64
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IssueQuestion",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "external_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("name", models.CharField(blank=True, default="", max_length=250)),
                ("question", models.CharField(max_length=1024)),
                (
                    "issue",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="issue.issue"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VoterIssueQuestionOpinion",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "external_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "rating",
                    models.DecimalField(decimal_places=10, default=0.0, max_digits=10),
                ),
                (
                    "issue_question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="issue.issuequestion",
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
