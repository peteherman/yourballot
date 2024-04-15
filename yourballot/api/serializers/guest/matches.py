from django.db.models import Avg
from rest_framework import serializers

from yourballot.api.serializers.candidate.position import CandidatePositionSerializer
from yourballot.candidate.models.candidate import Candidate
from yourballot.issue.models.issue import Issue
from yourballot.issue.models.issue_question import CandidateIssueQuestionOpinion
from yourballot.similarity.similarity import calculate_candidate_similarity_to_issue_views


class GuestCandidateMatchRequestSerializer(serializers.Serializer):
    zipcode = serializers.CharField(max_length=5)
    issue_views = serializers.DictField()


class GuestCandidateMatchResponseSerializer(serializers.ModelSerializer):
    position = CandidatePositionSerializer(many=False, read_only=True)
    similarity = serializers.SerializerMethodField()
    issue_views = serializers.SerializerMethodField()

    def get_similarity(self, candidate: Candidate) -> float:
        issue_views = self._context.get("issue_views", None)
        return calculate_candidate_similarity_to_issue_views(candidate, issue_views)

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
