from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class APITestCase(TestCase):

    def setUp(self) -> None:
        user, _ = User.objects.get_or_create(username="test-user")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        super().setUp()
