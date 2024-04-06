from typing import cast

from factory import SubFactory
from factory.django import DjangoModelFactory

from yourballot.candidate.models.candidate import Candidate
from yourballot.candidate.models.factories.candidate import CandidateFactory
from yourballot.issue.models.vector import CandidateVector


class CandidateVectorFactory(DjangoModelFactory):
    candidate: Candidate = cast(Candidate, SubFactory(CandidateFactory))

    class Meta:
        model = CandidateVector
