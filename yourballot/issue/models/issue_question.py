from uuid import uuid4

from django.db import models

from yourballot.candidate.models import Candidate
from yourballot.voter.models import Voter

from .issue import Issue


class IssueQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    external_id = models.UUIDField(null=False, default=uuid4, blank=False, unique=True, editable=False)
    name = models.CharField(max_length=250, null=False, blank=True, default="")
    question = models.CharField(max_length=1024, null=False, blank=False)
    issue = models.ForeignKey(Issue, on_delete=models.PROTECT, null=False)


class VoterIssueQuestionOpinion(models.Model):
    """
    Holds the information pertinent to a voter's response to a given IssueQuestion
    """

    id = models.BigAutoField(primary_key=True)
    external_id = models.UUIDField(null=False, default=uuid4, blank=False, unique=True, editable=False)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, null=False)
    issue_question = models.ForeignKey(IssueQuestion, on_delete=models.PROTECT, null=False)
    rating = models.DecimalField(null=False, default=0.0, max_digits=10, decimal_places=10)


class CandidateIssueQuestionOpinion(models.Model):
    """
    Holds the information pertinent to a candidate's response to a given IssueQuestion
    """

    id = models.BigAutoField(primary_key=True)
    external_id = models.UUIDField(null=False, default=uuid4, blank=False, unique=True, editable=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=False)
    issue_question = models.ForeignKey(IssueQuestion, on_delete=models.PROTECT, null=False)
    rating = models.DecimalField(null=False, default=0.0, max_digits=10, decimal_places=10)


class VoterIssue(models.Model):
    id = models.BigAutoField(primary_key=True)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, null=False)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, null=False)
    weight = models.DecimalField(null=False, default=0.0, max_digits=10, decimal_places=10)
