from typing import cast

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from yourballot.locality.models.factories.political_locality import PoliticalLocalityFactory
from yourballot.locality.models.political_locality import PoliticalLocality
from yourballot.locality.models.zipcode_locality import ZipcodeLocality


class ZipcodeLocalityFactory(DjangoModelFactory):
    zipcode: str = cast(str, Faker("zipcode"))
    political_locality = cast(PoliticalLocality, SubFactory(PoliticalLocalityFactory))

    class Meta:
        model = ZipcodeLocality
