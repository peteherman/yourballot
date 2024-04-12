from rest_framework import serializers

from yourballot.candidate.models.candidate import Candidate
from yourballot.similarity.similarity import calculate_voter_candidate_similarity
from yourballot.voter.models.voter import Voter


class VoterCandidateSerializer(serializers.ModelSerializer):
    similarity = serializers.SerializerMethodField()

    def get_similarity(self, candidate: Candidate) -> float:
        request = self._context.get("request", None)
        voter = Voter.objects.filter(user=request.user).first()
        if not voter:
            raise Exception(f"Request did not have an associated voter! {request}")
        return calculate_voter_candidate_similarity(voter, candidate)

    class Meta:
        model = Candidate
        fields = ["id", "external_id", "position", "name", "profile_photo", "similarity"]
