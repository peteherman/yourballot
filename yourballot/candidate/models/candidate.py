from uuid import uuid4

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from yourballot.party import PoliticalParty
from yourballot.voter.models import Ethnicity, Gender, Race

from .candidate_position import CandidatePosition


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=False)
    external_id = models.UUIDField(null=False, editable=False, default=uuid4, unique=True)
    name = models.CharField(max_length=1024, null=False, blank=False)
    age = models.PositiveIntegerField(null=False, validators=[MinValueValidator(1)])
    bio = models.CharField(max_length=250, null=False, default="", blank=True)
    days_served = models.PositiveIntegerField(null=False, default=0)
    ethnicity = models.CharField(max_length=32, choices=Ethnicity.choices)
    gender = models.CharField(max_length=32, choices=Gender.choices)
    political_identity = models.CharField(
        max_length=1024,
        help_text="The way a candidate may describe themselves politically. e.g. a left-leaning moderate",
    )
    political_party = models.CharField(
        max_length=1024,
        help_text="The party to which the candidate belongs. Independent, Republican, etc.",
        choices=PoliticalParty.choices,
    )
    position = models.ForeignKey(CandidatePosition, on_delete=models.PROTECT)
    url = models.URLField(max_length=250)
    twitter = models.URLField(max_length=250)
    facebook = models.URLField(max_length=250)


class CandidateRace(models.Model):
    voter = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=False)
    race = models.CharField(max_length=1024, choices=Race.choices, null=False)
