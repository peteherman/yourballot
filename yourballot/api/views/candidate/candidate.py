from typing import Any

from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from yourballot.api.core.response import ballot_response
from yourballot.api.serializers.candidate.authenticated_detailed import AuthenticateCandidateDetailedSerializer
from yourballot.candidate.models.candidate import Candidate


class CandidateViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = AuthenticateCandidateDetailedSerializer
    permissions = [permissions.IsAuthenticated]
    queryset = Candidate.objects.all()

    def retrieve(self, request: Request, pk: int) -> Response:
        candidate = self.get_queryset().get(id=pk)
        if not candidate:
            raise Exception("Candidate not found")
        serializer = self.serializer_class(candidate, context={"request": self.request})
        return ballot_response(serializer.data)
