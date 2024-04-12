from typing import cast
from uuid import UUID

from django.contrib.auth.models import User
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from yourballot.core.tests.factories.user import UserFactory
from yourballot.party import PoliticalParty
from yourballot.voter.models.voter import Ethnicity, Gender, Race, Voter


class VoterFactory(DjangoModelFactory):
    external_id: UUID = cast(UUID, Faker("uuid4"))
    age: int = cast(int, Faker("pyint", min_value=1, max_value=120))
    ethnicity: Ethnicity = cast(Ethnicity, FuzzyChoice(Ethnicity.choices))
    gender: Gender = cast(Gender, FuzzyChoice(Gender.choices))
    race: Race = cast(Race, FuzzyChoice(Race.choices))
    political_identity: str = cast(str, Faker("name"))
    political_party: PoliticalParty = cast(PoliticalParty, FuzzyChoice(PoliticalParty.choices))
    zipcode: str = cast(str, Faker("zipcode"))
    user: User = cast(User, SubFactory(UserFactory))

    class Meta:
        model = Voter
