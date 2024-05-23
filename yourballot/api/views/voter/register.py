from rest_framework import mixins, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from yourballot.api.core.response import ballot_response
from yourballot.api.serializers.voter.register import VoterRegistrationSerializer
from yourballot.voter.exceptions import VoterCreationFailureException
from yourballot.voter.models.voter import Voter
from yourballot.voter.service import VoterService


class VoterRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = VoterRegistrationSerializer
    queryset = Voter.objects.none()

    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return ballot_response(
                {}, success=False, errors=list(serializer.errors), status=status.HTTP_400_BAD_REQUEST
            )

        try:
            voter = VoterService.create_voter(serializer)
            return ballot_response({"id": voter.id}, status=status.HTTP_201_CREATED)
        except VoterCreationFailureException as e:
            return ballot_response({}, success=False, errors=[e.reason], status=status.HTTP_400_BAD_REQUEST)
