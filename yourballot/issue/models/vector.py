from uuid import uuid4

from django.db import models

from yourballot.candidate.models import Candidate
from yourballot.voter.models import Voter


class VoterVector(models.Model):
    id = models.BigAutoField(primary_key=True)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, null=False)
    external_id = models.UUIDField(null=False, default=uuid4, blank=False, unique=True, editable=False)
    immigration = models.FloatField(null=False, default=0.0)
    environment = models.FloatField(null=False, default=0.0)
    gun_control = models.FloatField(null=False, default=0.0)
    abortion = models.FloatField(null=False, default=0.0)
    healthcare = models.FloatField(null=False, default=0.0)


class CandidateVector(models.Model):
    id = models.BigAutoField(primary_key=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=False)
    external_id = models.UUIDField(null=False, default=uuid4, blank=False, unique=True, editable=False)
    immigration = models.FloatField(null=False, default=0.0)
    environment = models.FloatField(null=False, default=0.0)
    gun_control = models.FloatField(null=False, default=0.0)
    abortion = models.FloatField(null=False, default=0.0)
    healthcare = models.FloatField(null=False, default=0.0)
