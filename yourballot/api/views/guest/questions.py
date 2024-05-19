from typing import cast

from django.conf import settings
from django.db.models import QuerySet
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from yourballot.api.serializers.question import QuestionSerializer
from yourballot.issue.models.issue_question import IssueQuestion


class GuestQuestionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = QuestionSerializer
    queryset = IssueQuestion.objects.none()
    ordering = ["issue"]
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self) -> QuerySet:
        return IssueQuestion.objects.all()

    def list(self, request: Request) -> Response:
        queryset = self.get_queryset()
        limited_questions = queryset[0 : settings.GUEST_QUESTION_LIMIT]
        serializer = self.serializer_class(limited_questions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
