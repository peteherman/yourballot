# Generated by Django 5.0.3 on 2024-05-24 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter", "0006_alter_voter_ethnicity"),
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
                max_length=64,
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
                max_length=64,
                null=True,
            ),
        ),
    ]
