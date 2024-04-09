from rest_framework import serializers

from yourballot.api.serializers.locality import PoliticalLocalitySerializer
from yourballot.candidate.models.candidate_position import CandidatePosition


class CandidatePositionSerializer(serializers.ModelSerializer):
    locality = PoliticalLocalitySerializer(many=False, read_only=True)

    class Meta:
        model = CandidatePosition
        fields = ["id", "title", "locality", "term_limit"]
