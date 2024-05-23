from django.contrib.auth.models import User
from django.db import transaction

from yourballot.api.serializers.voter.register import VoterRegistrationSerializer
from yourballot.voter.exceptions import VoterCreationFailureException
from yourballot.voter.models.voter import Voter


class VoterService:

    @classmethod
    def create_voter(cls, serializer: VoterRegistrationSerializer) -> Voter:
        """
        Creates a django user and a Voter. Raises an exception if creating a voter fails
        """
        if not serializer.is_valid():
            raise VoterCreationFailureException(reason=", ".join(serializer.errors))

        voter: Voter | None = None
        with transaction.atomic():
            user_with_email = User.objects.filter(email=serializer.data.get("email"))
            if user_with_email.exists():
                raise VoterCreationFailureException(reason="This email address is in use")

            user = User.objects.create(
                email=serializer.data.get("email"),
                password=serializer.data.get("password"),
                username=serializer.data.get("email"),
                is_staff=False,
                is_active=True,
                is_superuser=False,
                first_name="",
                last_name="",
            )  # type: ignore
            voter = Voter.objects.create(
                user=user,
                age=serializer.data.get("age"),
                ethnicity=serializer.data.get("ethnicity"),
                gender=serializer.data.get("gender"),
                race=serializer.data.get("race"),
                political_identity=serializer.data.get("political_identity"),
                political_party=serializer.data.get("political_party"),
                zipcode=serializer.data.get("zipcode"),
            )  # type: ignore

        return voter
