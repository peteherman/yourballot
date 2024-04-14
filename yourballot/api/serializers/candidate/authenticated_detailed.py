from django.db.models import Avg
from rest_framework import serializers

from yourballot.api.serializers.candidate.position import CandidatePositionSerializer
from yourballot.candidate.models.candidate import Candidate
from yourballot.issue.models.issue import Issue
from yourballot.issue.models.issue_question import CandidateIssueQuestionOpinion
from yourballot.similarity.similarity import calculate_voter_candidate_similarity
from yourballot.voter.models.voter import Voter


class AuthenticateCandidateDetailedSerializer(serializers.ModelSerializer):
    position = CandidatePositionSerializer(many=False, read_only=True)
    similarity = serializers.SerializerMethodField()
    issue_views = serializers.SerializerMethodField()

    def get_similarity(self, candidate: Candidate) -> float:
        request = self._context.get("request", None)
        voter = Voter.objects.filter(user=request.user).first()
        if not voter:
            raise Exception(f"Request did not have an associated voter! {request}")
        return calculate_voter_candidate_similarity(voter, candidate)

    def get_issue_views(self, candidate: Candidate) -> dict[str, float]:
        all_issues = Issue.objects.all()
        issue_views: dict[str, float] = {}
        for issue in all_issues:
            issue_views[issue.name] = 0.0
        issue_aggregation_qs = (
            CandidateIssueQuestionOpinion.objects.filter(candidate=candidate)
            .values("issue_question__issue")
            .annotate(avg_rating=Avg("rating"))
            .values_list("issue_question__issue__name", "avg_rating", named=True)
        )

        for row in issue_aggregation_qs:
            issue_views[row.issue_question__issue__name] = row.avg_rating

        return issue_views

    class Meta:
        model = Candidate
        fields = [
            "id",
            "external_id",
            "name",
            "age",
            "bio",
            "start_date",
            "similarity",
            "ethnicity",
            "gender",
            "political_identity",
            "political_party",
            "position",
            "url",
            "profile_photo",
            "issue_views",
            "twitter",
            "facebook",
        ]
