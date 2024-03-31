from rest_framework import serializers

from yourballot.candidate.models.candidate import Candidate
from yourballot.candidate.models.candidate_position import CandidatePosition


class CandidateSerializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(required=True, queryset=CandidatePosition.objects.all())

    class Meta:
        model = Candidate
        fields = [
            "id",
            "external_id",
            "name",
            "age",
            "bio",
            "days_served",
            "ethnicity",
            "gender",
            "political_identity",
            "position",
            "url",
            "twitter",
            "facebook",
        ]
