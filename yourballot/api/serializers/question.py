from rest_framework import serializers

from yourballot.issue.models.issue_question import IssueQuestion


class QuestionSerializer(serializers.ModelSerializer):
    issue_name = serializers.SerializerMethodField()

    class Meta:
        model = IssueQuestion
        fields = ["id", "external_id", "name", "question", "issue", "issue_name"]

    def get_issue_name(self, obj: IssueQuestion) -> str | None:
        return obj.issue.name if obj.issue else None
