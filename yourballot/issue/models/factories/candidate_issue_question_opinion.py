import random
from typing import cast
from uuid import UUID

from factory import Faker, LazyFunction, SubFactory
from factory.django import DjangoModelFactory

from yourballot.candidate.models import Candidate
from yourballot.candidate.models.factories.candidate import CandidateFactory
from yourballot.issue.models.factories.issue_question import IssueQuestionFactory
from yourballot.issue.models.issue_question import CandidateIssueQuestionOpinion, IssueQuestion


class CandidateIssueQuestionOpinionFactory(DjangoModelFactory):
    external_id: UUID = cast(UUID, Faker("uuid4"))
    candidate: Candidate = cast(Candidate, SubFactory(CandidateFactory))
    issue_question: IssueQuestion = cast(IssueQuestion, SubFactory(IssueQuestionFactory))
    rating: float = cast(float, LazyFunction(lambda: round(random.uniform(1, 10), 3)))

    class Meta:
        model = CandidateIssueQuestionOpinion
