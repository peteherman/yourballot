# Generated by Django 5.0.3 on 2024-04-06 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("issue", "0006_remove_votervector_voter_delete_candidatevector_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voterissue",
            name="weight",
            field=models.DecimalField(decimal_places=10, default=1.0, max_digits=10),
        ),
    ]