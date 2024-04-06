from typing import cast

from factory import SubFactory
from factory.django import DjangoModelFactory

from yourballot.issue.models.vector import VoterVector
from yourballot.voter.models.factories.voter import VoterFactory
from yourballot.voter.models.voter import Voter


class VoterVectorFactory(DjangoModelFactory):
    voter: Voter = cast(Voter, SubFactory(VoterFactory))

    class Meta:
        model = VoterVector
