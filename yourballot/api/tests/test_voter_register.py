from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

from yourballot.core.tests.factories.user import UserFactory
from yourballot.voter.models.voter import Voter


class TestVoterRegister(APITestCase):
    url = "/v1/voter/register/"
    email = "test@mail.com"

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()

    def validate_user_and_voter_created(self, email: str, response: Response) -> None:
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Received unexpected status. Expected 201")
        voter_result = response.json().get("result")
        self.assertIsNotNone(voter_result, "'result' did not exist in the response")
        voter_id = voter_result.get("id")
        self.assertIsNotNone(voter_id, "'id' for voter did not exist in 'result' in response")

        voters = Voter.objects.filter(id=voter_id)
        self.assertTrue(voters.exists(), f"Voter object with id {voter_id} did not exist")
        voter = voters.first()
        user = voter.user
        self.assertEqual(user.email, email, f"Email used to register and the email of the created user do not match")

    def test_voter_creation_when_no_voter_exists(self) -> None:
        body = {
            "email": self.email,
            "zipcode": "12345",
            "password": "Password",
            "political_identity": "",
        }

        response = self.client.post(self.url, body, format="json")
        self.validate_user_and_voter_created(self.email, response)

    def test_voter_creation_fails_when_user_with_email_already_exists(self) -> None:
        _ = UserFactory.create(email=self.email)

        self.assertEqual(User.objects.count(), 1)
        body = {
            "email": self.email,
            "zipcode": "12831",
            "password": "Password",            
            "political_identity": "",
        }

        response = self.client.post(self.url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_messages = response.json().get("result_info", {}).get("errors")
        self.assertTrue(
            any(
                "email address is in use" in error_msg.lower()
                for error_msg in error_messages
            ), f"Did not find expected error message in response errors: {error_messages}"
        )

    def test_voter_creation_fails_when_request_body_malformed(self) -> None:
        body = {
            "email": "invalid",
            "zipcode": "12831",
            "password": "Password",            
            "political_identity": "",
        }
        response = self.client.post(self.url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
