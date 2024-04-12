from typing import cast

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import filters, mixins, permissions, viewsets

from yourballot.api.serializers.voter.candidate import VoterCandidateSerializer
from yourballot.candidate.models.candidate import Candidate
from yourballot.locality.models.zipcode_locality import ZipcodeLocality
from yourballot.voter.models.voter import Voter


class VoterCandidateViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = VoterCandidateSerializer
    queryset = Candidate.objects.all()
    permissions = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ["id"]

    def get_queryset(self) -> QuerySet:
        user = cast(User, self.request.user)
        voter = Voter.objects.get(user=user)

        return Candidate.objects.filter(
            position__locality__in=ZipcodeLocality.objects.filter(zipcode=voter.zipcode).values("political_locality")
        )
