# Generated by Django 5.0.3 on 2024-03-12 00:59

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Voter",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "external_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "age",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                limit_value=1, message="Minimum age is 1 year(s) old"
                            )
                        ]
                    ),
                ),
                (
                    "ethnicity",
                    models.CharField(
                        choices=[
                            ("HISPANIC_OR_LATINO", "Hispanic or Latino"),
                            ("NOT_HISPANIC_OR_LATINO", "Not Hispanic or Latino"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("FEMALE", "Female"),
                            ("MALE", "Male"),
                            ("Transgender", "Transgender"),
                            ("NONBINARY", "Nonbinary"),
                            ("OTHER", "Other"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "political_identity",
                    models.CharField(
                        help_text="The way a voter may describe themselves politically. e.g. a left-leaning moderate",
                        max_length=1024,
                    ),
                ),
                (
                    "political_party",
                    models.CharField(
                        choices=[
                            ("DEMOCRATIC", "Democratic Party"),
                            ("REPUBLICAN", "Republican Party"),
                            ("INDEPENDENT", "Independent"),
                            ("LIBERTARIAN", "Libertarian Party"),
                            ("FORWARD", "Forward"),
                            ("VERMONT_PROGRESSIVE", "Vermont Progressive Party"),
                            ("INDEPENDENT_OF_OREGON", "Independent Party of Oregon"),
                            ("GREEN", "Green Party"),
                            ("CONSTITUTION", "Constitution Party"),
                            ("WORKING_FAMILIES", "Working Families Party"),
                            ("ALLIANCE", "Alliance Party"),
                            ("REFORM", "Reform Party"),
                            ("WORKING_CLASS", "Working Class Party"),
                            (
                                "SOCIALISM_LIBERATION",
                                "Party for Socialism and Liberation",
                            ),
                            (
                                "AMERICAN_INDEPENDENT_PARTY",
                                "American Independent Party",
                            ),
                            ("PEACE_FREEDOM", "Peace and Freedom Party"),
                            ("SOLIDARITY", "American Solidarity Party"),
                            ("LEGAL_MARIJUANA", "Legal Marijuana Now Party"),
                            ("UNITY_PARTY", "Unity Party"),
                            ("NATURAL_LAW", "Natural Law Party"),
                            ("APPROVAL_VOTING", "Approval Voting Party"),
                            ("JUSTICE", "Justice Party"),
                            ("PEOPLE", "People's Party"),
                            ("COLORADO_CENTER", "Colorado Center Party"),
                            ("CONSERVATIVE_NY", "Conservative Party of New York State"),
                            (
                                "LIBERTARIAN_MASS",
                                "Libertarian Association of Massachusetts",
                            ),
                            ("LIBERTARIAN_NM", "Libertarian Party of New Mexico"),
                            ("OREGON_PROGRESSIVE", "Oregon Progressive Party"),
                            (
                                "GREEN_MOUNTAIN",
                                "Green Mountain Peace and Justice Party",
                            ),
                            ("ALASKAN_INDEPENDENCE", "Alaskan Independence Party"),
                            ("INDEPENDENT_DELAWARE", "Independent Party of Delaware"),
                            ("UNITED_UTAH", "United Utah Party"),
                            ("ECOLOGY_FLORIDA", "Ecology Party of Florida"),
                            ("INDEPENDENT_FLORIDA", "Independent Party of Florida"),
                            ("ALOHA", "Aloha Party"),
                            (
                                "GRASSROOTS_CANNABIS",
                                "Grassroots - Legalize Cannabis Party",
                            ),
                            ("LABOR", "Labor Party"),
                            ("UNITED_CITIZENS", "United Citizens Party"),
                            ("INDEPENDENT_CITIZENS", "Independent Citizens Movement"),
                            ("SOVEREIGN_UNION", "Sovereign Union Movement"),
                            ("SOCIALIST_WORKERS", "Socialist Workers Party"),
                            ("PROHIBITION", "Prohibition Party"),
                            ("SOCIALIST_EQUALITY", "Socialist Equality Party"),
                            ("SOCIALIST_USA", "Socialist Party USA"),
                            ("COMMUNIST", "Communist Party USA"),
                            ("PROGRESSIVE_LABOR", "Progressive Labor Party"),
                            ("SOCIALIST_ALTERNATIVE", "Socialist Alternative"),
                            ("PIRATE", "United States Pirate Party"),
                            ("WORKERS_WORLD", "Workers World Party"),
                            ("FREEDOM_SOCIALIST", "Freedom Socialist Party"),
                            ("AMERICAN_FREEDOM", "American Freedom Party"),
                            ("SOCIALIST_ACTION", "Socialist Action"),
                            ("TRANSHUMANIST", "Transhumanist Party"),
                        ],
                        help_text="The party to which the voter is registered. Independent, Republican, etc.",
                        max_length=1024,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VoterRace",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "race",
                    models.CharField(
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
                        max_length=1024,
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
