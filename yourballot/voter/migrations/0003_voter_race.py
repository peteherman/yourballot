# Generated by Django 5.0.3 on 2024-03-20 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter", "0002_alter_voter_age_alter_voter_ethnicity_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="voter",
            name="race",
            field=models.CharField(
                choices=[
                    (
                        "AMERICAN_INDIAN_OR_ALASKA_NATIVE",
                        "American Indian or Alaska Native",
                    ),
                    ("ASIAN", "Asian"),
                    ("BLACK_OR_AFRICAN_AMERICAN", "Black or African American"),
                    (
                        "NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER",
                        "Native Hawaiian or Other Pacific Islander",
                    ),
                    ("WHITE", "White"),
                ],
                max_length=64,
                null=True,
            ),
        ),
    ]
