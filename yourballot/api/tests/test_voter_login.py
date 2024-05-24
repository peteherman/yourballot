from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from yourballot.voter.models.factories.voter import VoterFactory
from yourballot.voter.models.voter import Voter


class TestVoterLoginViewSet(APITestCase):
    email = "test@mail.com"
    password = "MyPassword123!"
    url = "/v1/voter/login/"

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()

    def test_authentication_fails_when_no_user_present(self) -> None:
        body = {
            "email": self.email,
            "password": self.password,
        }

        response = self.client.post(self.url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication_fails_when_password_incorrect(self) -> None:
        user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
        voter = VoterFactory.create(user=user)

        body = {
            "email": self.email,
            "password": "incorrect password",
        }

        response = self.client.post(self.url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication_fails_when_email_doesnt_exist(self) -> None:
        user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
        voter = VoterFactory.create(user=user)

        body = {
            "email": "wrongemail@mail.com",
            "password": self.password,
        }

        response = self.client.post(self.url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication_fails_when_no_voter_is_found_for_user(self) -> None:
        user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
        body = {
            "email": self.email,
            "password": self.password,
        }

        response = self.client.post(self.url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication_succeeds_when_user_and_password_correct(self) -> None:
        user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
        voter = VoterFactory.create(user=user)
        body = {
            "email": self.email,
            "password": self.password,
        }

        response = self.client.post(self.url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate access and refresh tokens were included in the response
        result = response.json().get("result")
        self.assertIsNotNone(result)
        access_token = result.get("access")
        self.assertIsNotNone(access_token, "Expected response result to contain 'access' token")
        refresh_token = result.get("refresh")
        self.assertIsNotNone(refresh_token, "Expected response result to contain 'refresh' token")
