# Generated by Django 5.0.3 on 2024-04-05 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("candidate", "0003_candidate_profile_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidate",
            name="facebook",
            field=models.URLField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="profile_photo",
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="twitter",
            field=models.URLField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="url",
            field=models.URLField(max_length=250, null=True),
        ),
    ]
