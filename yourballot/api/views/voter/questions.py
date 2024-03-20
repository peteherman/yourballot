from typing import cast

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from yourballot.api.serializers.question import QuestionSerializer
from yourballot.issue.models.issue_question import IssueQuestion, VoterIssueQuestionOpinion
from yourballot.voter.models import Voter


class VoterQuestionRemainingViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = QuestionSerializer
    queryset = IssueQuestion.objects.none()
    permissions = [permissions.IsAuthenticated]
    ordering = ["issue"]
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self) -> QuerySet:
        user = cast(User, self.request.user)
        voter = Voter.objects.get(user=user)
        return IssueQuestion.objects.all().exclude(
            id__in=VoterIssueQuestionOpinion.objects.filter(voter=voter).values("voter")
        )

    def list(self, request: Request) -> Response:
        return super().list(request)
