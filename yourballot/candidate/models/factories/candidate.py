from datetime import datetime, timedelta, timezone
from typing import cast
from uuid import UUID

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from yourballot.candidate.models.candidate import Candidate
from yourballot.candidate.models.candidate_position import CandidatePosition
from yourballot.candidate.models.factories.candidate_position import CandidatePositionFactory
from yourballot.party import PoliticalParty
from yourballot.voter.models import Ethnicity, Gender, Race


class CandidateFactory(DjangoModelFactory):
    external_id: UUID = cast(UUID, Faker("uuid4"))
    age: int = cast(int, Faker("pyint", min_value=1, max_value=120))
    name: str = cast(str, Faker("name"))
    bio: str = cast(str, Faker("sentence"))
    start_date: datetime = cast(datetime, Faker("date_time_this_decade", tzinfo=timezone(timedelta(hours=5))))
    ethnicity: Ethnicity = cast(Ethnicity, FuzzyChoice(Ethnicity.choices))
    gender: Gender = cast(Gender, FuzzyChoice(Gender.choices))
    political_identity: str = cast(str, Faker("name"))
    political_party: PoliticalParty = cast(PoliticalParty, FuzzyChoice(PoliticalParty.choices))
    position: CandidatePosition = cast(CandidatePosition, SubFactory(CandidatePositionFactory))
    url: str = cast(str, Faker("url"))
    twitter: str = cast(str, Faker("url"))
    facebook: str = cast(str, Faker("url"))
    profile_photo: str = cast(str, Faker("url"))

    class Meta:
        model = Candidate
