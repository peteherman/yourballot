import logging
from typing import Any

from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from yourballot.api.core.response import ballot_response
from yourballot.api.serializers.candidate.authenticated_detailed import \
    AuthenticateCandidateDetailedSerializer
from yourballot.candidate.models.candidate import Candidate
from yourballot.voter.models.voter import Voter


class CandidateViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = AuthenticateCandidateDetailedSerializer
    permissions = [permissions.IsAuthenticated]
    queryset = Candidate.objects.all()

    def _get_voter(self, request: Request) -> Voter:
        user = self.request.user
        if not user:
            raise Exception("No user on request!")
        voter = Voter.objects.filter(user=user).first()  # type: ignore
        if not voter:
            raise Exception("Unable to identify Voter for request!")
        return voter

    def retrieve(self, request: Request, pk: int) -> Response:
        candidate = self.get_queryset().get(id=pk)
        if not candidate:
            raise Exception("Candidate not found")

        voter = self._get_voter(request)
        serializer = self.serializer_class(candidate, context={"voter": voter})
        return ballot_response(serializer.data)
