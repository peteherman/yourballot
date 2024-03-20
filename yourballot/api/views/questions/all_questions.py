from rest_framework import mixins, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from yourballot.api.serializers.question import QuestionSerializer
from yourballot.issue.models.issue_question import IssueQuestion


class AllQuestionsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = QuestionSerializer
    queryset = IssueQuestion.objects.all().order_by("issue")

    def list(self, request: Request) -> Response:
        return super().list(request)
