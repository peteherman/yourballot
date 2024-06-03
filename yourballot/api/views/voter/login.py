from http import HTTPMethod

from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from yourballot.api.core.response import ballot_response
from yourballot.api.serializers.voter.login import VoterLoginSerializer
from yourballot.voter.models.voter import Voter


class VoterLoginViewSet(viewsets.GenericViewSet):
    queryset = Voter.objects.none()
    serializer_class = VoterLoginSerializer

    @action(detail=False, methods=["POST"])
    def login(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        errors: list[str] = []
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            if email:
                email = email.lower()
            user = authenticate(
                username=email, password=serializer.validated_data.get("password")
            )
            if user is not None:
                voter = Voter.objects.filter(user=user).first()  # type: ignore
                if voter:
                    refresh = RefreshToken.for_user(voter.user)
                    return ballot_response(
                        {
                            "id": voter.id,
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),  # type: ignore
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    errors.append("Unable to find your account")
            else:
                errors.append("Unable to authenticate your request")
        else:
            errors.append("Malformed request: " + ", ".join(serializer.errors))
        return ballot_response({}, errors=errors, success=False, status=status.HTTP_401_UNAUTHORIZED)
