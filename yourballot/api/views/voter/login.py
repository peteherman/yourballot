from http import HTTPMethod

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from yourballot.api.core.response import ballot_response
from yourballot.api.serializers.voter.login import VoterLoginSerializer
from yourballot.voter.models.voter import Voter


class VoterLoginViewSet(viewsets.GenericViewSet):
    queryset = Voter.objects.none()
    serializer_class = VoterLoginSerializer

    @action(detail=False, methods=[HTTPMethod.POST])
    def login(self, request: Request) -> Response:
        return ballot_response({}, status=status.HTTP_400_BAD_REQUEST)
