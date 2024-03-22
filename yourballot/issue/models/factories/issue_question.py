import random
from typing import cast
from uuid import UUID

from factory import Faker, LazyFunction, SubFactory
from factory.django import DjangoModelFactory

from yourballot.issue.models.factories.issue import IssueFactory
from yourballot.issue.models.issue import Issue
from yourballot.issue.models.issue_question import IssueQuestion, VoterIssueQuestionOpinion
from yourballot.voter.models import Voter
from yourballot.voter.models.factories.voter import VoterFactory


class IssueQuestionFactory(DjangoModelFactory):
    issue: Issue = cast(Issue, SubFactory(IssueFactory))

    class Meta:
        model = IssueQuestion


class VoterIssueQuestionOpinionFactory(DjangoModelFactory):
    external_id: UUID = cast(UUID, Faker("uuid4"))
    voter: Voter = cast(Voter, SubFactory(VoterFactory))
    issue_question: IssueQuestion = cast(IssueQuestion, SubFactory(IssueQuestionFactory))
    rating: float = cast(float, LazyFunction(lambda: round(random.uniform(1, 10), 3)))

    class Meta:
        model = VoterIssueQuestionOpinion
