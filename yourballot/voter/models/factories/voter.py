from factory.django import DjangoModelFactory

from yourballot.voter.models.voter import Voter


class VoterFactory(DjangoModelFactory):

    class Meta:
        model = Voter
