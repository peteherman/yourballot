from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from yourballot.api.serializers.question import QuestionSerializer
from yourballot.issue.models.issue_question import IssueQuestion


class AllQuestionsViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = IssueQuestion.objects.all()

    def list(self, request: Request) -> Response:
        return Response({}, status=status.HTTP_200_OK)
