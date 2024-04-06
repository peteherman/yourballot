from factory.django import DjangoModelFactory

from yourballot.locality.models.political_locality import PoliticalLocality


class PoliticalLocalityFactory(DjangoModelFactory):
    class Meta:
        model = PoliticalLocality
