from rest_framework import serializers

from yourballot.voter.models.voter import Voter


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
