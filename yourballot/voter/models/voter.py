from uuid import uuid4

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from yourballot.party import PoliticalParty


class Ethnicity(models.TextChoices):
    HISPANIC_OR_LATINO = "hispanic_or_latino", _("Hispanic or Latino")
    NOT_HISPANIC_OR_LATINO = "not_hispanic_or_latino", _("Not Hispanic or Latino")


class Race(models.TextChoices):
    AMERICAN_INDIAN_OR_ALASKA_NATIVE = "american_indian_or_alaska_native", _("American Indian or Alaska Native")
    ASIAN = "asian", _("Asian")
    BLACK_OR_AFRICAN_AMERICAN = "black_or_african_american", _("Black or African American")
    NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER = "native_hawaiian_or_pacific_islander", _(
        "Native Hawaiian or Other Pacific Islander"
    )
    WHITE = "white", _("White")


class Gender(models.TextChoices):
    FEMALE = "female", _("Female")
    MALE = "male", _("Male")
    TRANSGENDER = "transgender", _("Transgender")
    NONBINARY = "nonbinary", _("Nonbinary")
    OTHER = "other", _("Other")


class Voter(models.Model):
    id = models.BigAutoField(primary_key=True)
    external_id = models.UUIDField(null=False, unique=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=False)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(limit_value=1, message="Minimum age is 1 year(s) old")], null=True
    )
    ethnicity = models.CharField(max_length=32, choices=Ethnicity.choices, null=True)
    gender = models.CharField(max_length=32, choices=Gender.choices, null=True)
    race = models.CharField(max_length=64, choices=Race.choices, null=True)
    political_identity = models.CharField(
        max_length=1024,
        help_text="The way a voter may describe themselves politically. e.g. a left-leaning moderate",
        null=False,
        blank=True,
    )
    political_party = models.CharField(
        max_length=1024,
        help_text="The party to which the voter is registered. Independent, Republican, etc.",
        choices=PoliticalParty.choices,
        null=True,
    )
    zipcode = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{5}$',
                message='Zip code must be in the format XXXXX'
            )
        ]
    )

    def __str__(self) -> str:
        return f"Voter: {self.id} - {self.political_party}"


class VoterRace(models.Model):
    id = models.BigAutoField(primary_key=True)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, null=False)
    race = models.CharField(max_length=1024, choices=Race.choices, null=False)
