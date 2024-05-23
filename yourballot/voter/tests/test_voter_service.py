from typing import Any, cast

from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from yourballot.core.test.factories.user import UserFactory
from yourballot.voter.models.factories.voter import VoterFactory
from yourballot.voter.models.voter import Voter


class TestVoterService(APITestCase):
    url = "v1/voter/register/"

    def setUp(self) -> None:
        self.client = APIClient()
        self.request_factory = APIRequestFactory()

    def validate_user_and_voter_created(self, voter_id: int, registration_body: dict[str, Any]) -> None:
        """
        Verify both the voter and the user where created
        """
        voter = Voter.objects.filter(id=voter_id).first()
        self.assertIsNotNone(voter, "Voter failed to be created")
        self.assertEqual(registration_body.get("email"), voter.user.email)

    def test_voter_creation_succeeds_when_no_voters_or_users_exist(self) -> None:
        """
        Test voter creation succeeds with empty state
        """
        voter_registration_body = {
            "age": None,
            "ethnicity": None,
            "gender": None,
            "race": None,
            "political_identity": None,
            "political_party": None,
            "zipcode": "12831",
            "email": "test@mail.com",
            "password": "Password",
        }

        response = self.client.post(self.url, voter_registration_body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = response.get("result")
        self.assertIsNotNone(result)
        voter_id = cast(int | None, result.get("id"))
        self.assertIsNotNone(voter_id)
        self.validate_user_and_voter_created(voter_id, voter_registration_body)

    def test_voter_creation_fails_when_no_email_is_provided(self) -> None:
        """
        Test voter creation succeeds with empty state
        """
        voter_registration_body = {
            "age": None,
            "ethnicity": None,
            "gender": None,
            "race": None,
            "political_identity": None,
            "political_party": None,
            "zipcode": "12831",
            "email": "test@mail.com",
            "password": "Password",
        }
        
        response = self.client.post(self.url, voter_registration_body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = response.get("result")
        self.assertIsNotNone(result)
        voter_id = cast(int | None, result.get("id"))
        self.assertIsNotNone(voter_id)
        self.validate_user_and_voter_created(voter_id, voter_registration_body)
