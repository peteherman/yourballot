from typing import Any, cast

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from yourballot.api.serializers.voter.register import VoterRegistrationSerializer
from yourballot.core.tests.factories.user import UserFactory
from yourballot.voter.exceptions import VoterCreationFailureException
from yourballot.voter.models.factories.voter import VoterFactory
from yourballot.voter.models.voter import Voter
from yourballot.voter.service import VoterService


class TestVoterService(APITestCase):
    url = "v1/voter/register/"

    def setUp(self) -> None:
        self.client = APIClient()
        self.request_factory = APIRequestFactory()

    def validate_user_and_voter_created(self, voter: Voter, registration_body: dict[str, Any]) -> None:
        """
        Verify both the voter and the user where created
        """
        self.assertIsNotNone(voter, "Voter failed to be created")
        self.assertEqual(registration_body.get("email"), voter.user.email)

    def test_voter_creation_succeeds_when_no_voters_or_users_exist(self) -> None:
        """
        Test voter creation succeeds with empty state
        """
        voter_registration_body = {
            "zipcode": "12831",
            "email": "test@mail.com",
            "password": "Password",
            "political_identity": "",
        }

        serializer = VoterRegistrationSerializer(data=voter_registration_body)
        voter = VoterService.create_voter(serializer)
        self.assertIsNotNone(voter)
        self.validate_user_and_voter_created(voter, voter_registration_body)

    def test_voter_creation_fails_when_serializer_is_invalid(self) -> None:
        voter_registration_body = {
            "zipcode": "12831",
            "email": "invalid",
            "password": "Password",
            "political_identity": "",            
        }

        serializer = VoterRegistrationSerializer(data=voter_registration_body)

        with self.assertRaises(VoterCreationFailureException):
            VoterService.create_voter(serializer)

    def test_voter_creation_fails_when_user_with_email_already_exists(self) -> None:
        # Create existing user
        email_address = "test@mail.com"
        user = UserFactory.create(email=email_address)

        self.assertEqual(User.objects.count(), 1)

        voter_registration_body = {
            "zipcode": "12831",
            "email": email_address,
            "password": "Password",
            "political_identity": "",            
        }

        serializer = VoterRegistrationSerializer(data=voter_registration_body)

        with self.assertRaises(VoterCreationFailureException):
            VoterService.create_voter(serializer)

        self.assertEqual(User.objects.count(), 1)
