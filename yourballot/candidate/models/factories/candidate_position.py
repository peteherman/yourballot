from typing import cast

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from yourballot.candidate.models.candidate_position import CandidatePosition
from yourballot.locality.models.factories.political_locality import PoliticalLocalityFactory
from yourballot.locality.models.political_locality import PoliticalLocality


class CandidatePositionFactory(DjangoModelFactory):
    title: str = cast(str, Faker("name"))
    locality: PoliticalLocality = cast(PoliticalLocality, SubFactory(PoliticalLocalityFactory))
    term_limit: int = cast(int, Faker("pyint", min_value=1, max_value=730))

    class Meta:
        model = CandidatePosition
