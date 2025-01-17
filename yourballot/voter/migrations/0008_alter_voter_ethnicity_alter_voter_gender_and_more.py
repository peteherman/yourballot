# Generated by Django 5.0.3 on 2024-05-24 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter", "0007_alter_voter_ethnicity_alter_voter_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="ethnicity",
            field=models.CharField(
                choices=[
                    ("Hispanic or Latino", "Hispanic Or Latino"),
                    ("Not Hispanic or Latino", "Not Hispanic Or Latino"),
                ],
                max_length=128,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="voter",
            name="gender",
            field=models.CharField(
                choices=[
                    ("female", "Female"),
                    ("male", "Male"),
                    ("transgender", "Transgender"),
                    ("nonbinary", "Nonbinary"),
                    ("other", "Other"),
                ],
                max_length=128,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="voter",
            name="race",
            field=models.CharField(
                choices=[
                    (
                        "american_indian_or_alaska_native",
                        "American Indian or Alaska Native",
                    ),
                    ("asian", "Asian"),
                    ("black_or_african_american", "Black or African American"),
                    (
                        "native_hawaiian_or_pacific_islander",
                        "Native Hawaiian or Other Pacific Islander",
                    ),
                    ("white", "White"),
                ],
                max_length=128,
                null=True,
            ),
        ),
    ]
