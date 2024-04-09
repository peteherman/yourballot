from django.db.models import Avg, QuerySet
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from yourballot.api.serializers.voter.opinion_summary import VoterOpinionSummarySerializer
from yourballot.issue.models.issue_question import VoterIssueQuestionOpinion
from yourballot.voter.models import Voter


class VoterOpinionViewSet(viewsets.GenericViewSet):
    serializer_class = VoterOpinionSummarySerializer
    queryset = VoterIssueQuestionOpinion.objects.none()
    permissions = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        if not user:
            raise Exception("No user on request!")
        return Voter.objects.filter(user=user).first()  # type: ignore

    @action(detail=False, methods=["GET"])
    def summary(self, request: Request) -> Response:

        serializer = self.serializer_class(self.get_queryset())
        return Response(serializer.data)
