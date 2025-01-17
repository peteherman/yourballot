# Generated by Django 5.0.6 on 2024-05-29 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0008_alter_candidate_ethnicity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='ethnicity',
            field=models.CharField(choices=[('Hispanic or Latino', 'Hispanic Or Latino'), ('Not Hispanic or Latino', 'Not Hispanic Or Latino'), ('Choose not to share', 'Choose Not To Share')], max_length=32),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='gender',
            field=models.CharField(choices=[('female', 'Female'), ('male', 'Male'), ('transgender', 'Transgender'), ('nonbinary', 'Nonbinary'), ('other', 'Other'), ('choose_not_to_share', 'Choose not to share')], max_length=32),
        ),
        migrations.AlterField(
            model_name='candidaterace',
            name='race',
            field=models.CharField(choices=[('american_indian_or_alaska_native', 'American Indian or Alaska Native'), ('asian', 'Asian'), ('black_or_african_american', 'Black or African American'), ('native_hawaiian_or_pacific_islander', 'Native Hawaiian or Other Pacific Islander'), ('white', 'White'), ('choose_not_to_share', 'Choose Not to Share')], max_length=1024),
        ),
    ]
