import logging
from typing import cast

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from yourballot.api.serializers.question import VoterQuestionAnswerSerializer
from yourballot.issue.models.issue_question import VoterIssueQuestionOpinion
from yourballot.voter.models import Voter

logger = logging.getLogger(__name__)


class VoterAnswerQuestionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = VoterQuestionAnswerSerializer
    queryset = VoterIssueQuestionOpinion.objects.none()
    permissions = [permissions.IsAuthenticated]

    def create(self, request: Request) -> Response:
        user = cast(User, self.request.user)
        voter = Voter.objects.get(user=user)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                answered_question, created = VoterIssueQuestionOpinion.objects.get_or_create(
                    issue_question=serializer.validated_data.get("issue_question"),
                    voter=voter,
                    defaults={
                        "rating": serializer.validated_data.get("rating"),
                    },
                )
                if not created:
                    answered_question.rating = serializer.validated_data.get("rating")
                    answered_question.save()
            return Response({}, status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
