from functools import cached_property
from uuid import uuid4

from django.db import models

from yourballot.candidate.models import Candidate
from yourballot.similarity.similarity import euclidean_distance
from yourballot.voter.models import Voter

max_rating: float = 10.0


class BaseVector(models.Model):
    id = models.BigAutoField(primary_key=True)
    external_id = models.UUIDField(null=False, default=uuid4, blank=False, unique=True, editable=False)
    immigration = models.FloatField(null=False, default=0.0)
    environment = models.FloatField(null=False, default=0.0)
    gun_control = models.FloatField(null=False, default=0.0)
    abortion = models.FloatField(null=False, default=0.0)
    healthcare = models.FloatField(null=False, default=0.0)

    class Meta:
        abstract = True

    @classmethod
    def vector_fields(cls) -> list[models.fields.FloatField]:
        return [field for field in cls._meta.fields if isinstance(field, models.fields.FloatField)]

    @cached_property
    def max_euclidean_distance(self) -> float:
        max_vector = tuple([max_rating for _ in self.vector_fields()])
        min_vector = tuple([-max_rating for _ in self.vector_fields()])

        return euclidean_distance(max_vector, min_vector)

    def convert_to_vector_tuple(self) -> tuple[float, ...]:
        """
        Converts a vector (django) model class into a tuple of floats, for use in vector calculations
        Float fields are added to the tuple in alphabetical order to ensure consistency of ordering
        """
        vector_field_map: dict[str, float] = {}
        for field in self._meta.fields:
            if isinstance(field, models.fields.FloatField):
                vector_field_map[field.name] = field.value_from_object(self)
        vector_list = [vector_field_map[key] for key in sorted(vector_field_map.keys())]
        return tuple(vector_list)

    def similarity(self, other: "BaseVector") -> float:
        """
        Returns the similarity of two vectors using the following formula:
          abs(euclidean_distance(vector_a, vector_b) * cosine_similarity(vector_a, vector_b)) / MAX_EUCLIDEAN_DISTANCE
        """
        vector_a_tuple: tuple[float, ...] = self.convert_to_vector_tuple()
        vector_b_tuple: tuple[float, ...] = other.convert_to_vector_tuple()
        dist = euclidean_distance(vector_a_tuple, vector_b_tuple)
        return 1 - (dist / self.max_euclidean_distance)


class VoterVector(BaseVector):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, null=False)


class CandidateVector(BaseVector):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=False)
