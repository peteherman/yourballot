from django.db.models import Avg
from rest_framework import serializers

from yourballot.issue.models.issue import Issue
from yourballot.issue.models.issue_question import VoterIssue, VoterIssueQuestionOpinion
from yourballot.voter.models.voter import Voter


class VoterOpinionSummarySerializer(serializers.ModelSerializer):
    issue_views = serializers.SerializerMethodField()

    def get_issue_views(self, voter: Voter) -> dict[str, float]:
        all_issues = Issue.objects.all()
        issue_views: dict[str, float] = {}
        for issue in all_issues:
            issue_views[issue.name] = 0.0

        voter_avg_issue_opinion = (
            VoterIssueQuestionOpinion.objects.filter(voter=voter)
            .values("issue_question__issue")
            .annotate(avg_rating=Avg("rating"))
            .values_list("issue_question__issue__name", "avg_rating", named=True)
        )
        for issue_rating in voter_avg_issue_opinion:
            issue_views[issue_rating.issue_question__issue__name] = issue_rating.avg_rating

        for issue_weight in VoterIssue.objects.filter(voter=voter):
            issue_views[issue_weight.issue.name] *= issue_weight.weight
        return issue_views

    class Meta:
        model = Voter
        fields = ["issue_views"]
