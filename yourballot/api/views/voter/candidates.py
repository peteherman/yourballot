import logging
from typing import cast

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import filters, mixins, permissions, viewsets

from yourballot.api.serializers.candidate.authenticated_detailed import \
    AuthenticateCandidateDetailedSerializer
from yourballot.candidate.models.candidate import Candidate
from yourballot.locality.models.zipcode_locality import ZipcodeLocality
from yourballot.voter.models.voter import Voter

logger = logging.getLogger(__file__)


class VoterCandidateViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AuthenticateCandidateDetailedSerializer
    queryset = Candidate.objects.all()
    permissions = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ["id"]

    def get_queryset(self) -> QuerySet:
        user = cast(User, self.request.user)
        logger.warning("User: ", user)
        logger.warning("User email: ", user.email)
        voter = Voter.objects.get(user=user)

        return Candidate.objects.filter(
            position__locality__in=ZipcodeLocality.objects.filter(zipcode=voter.zipcode).values("political_locality")
        )
