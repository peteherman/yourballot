from django.db.models import QuerySet
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from yourballot.api.core.response import ballot_response
from yourballot.api.serializers.voter.profile import VoterProfileSerializer
from yourballot.voter.models.voter import Voter


class VoterProfileViewSet(viewsets.GenericViewSet):

    serializer_class = VoterProfileSerializer
    queryset = Voter.objects.none()
    permissions = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        if not user:
            raise Exception("No user on request!")
        return Voter.objects.filter(user=user).first()  # type: ignore

    @action(detail=False, methods=["GET"])
    def profile(self, request: Request) -> Response:
        serializer = self.serializer_class(self.get_queryset())
        return ballot_response(serializer.data)
