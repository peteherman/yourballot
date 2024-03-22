from rest_framework import serializers

from yourballot.issue.models.issue_question import IssueQuestion, VoterIssueQuestionOpinion


class QuestionSerializer(serializers.ModelSerializer):
    issue_name = serializers.SerializerMethodField()

    class Meta:
        model = IssueQuestion
        fields = ["id", "external_id", "name", "question", "issue", "issue_name"]

    def get_issue_name(self, obj: IssueQuestion) -> str | None:
        return obj.issue.name if obj.issue else None


class VoterQuestionAnswerSerializer(serializers.ModelSerializer):
    issue_question = serializers.PrimaryKeyRelatedField(required=True, queryset=IssueQuestion.objects.all())
    rating = serializers.FloatField(required=True, max_value=10.0, min_value=0.0)

    class Meta:
        model = VoterIssueQuestionOpinion
        fields = ["issue_question", "rating"]
