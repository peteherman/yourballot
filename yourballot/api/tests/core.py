from typing import Any, cast

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class APITestCase(TestCase):

    def setUp(self) -> None:
        user, _ = User.objects.get_or_create(username="test-user")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        super().setUp()

    def validate_pagination(
        self, response_data: dict[str, Any], total: int = 0, has_next: bool = False, has_prev: bool = False
    ) -> None:
        self.assertIsNotNone(response_data.get("result_info"))
        pagination_data = cast(dict, response_data.get("result_info"))

        self.assertIsNotNone(response_data.get("result"))
        self.assertEqual(pagination_data.get("total"), total)
        if has_next:
            self.assertIsNotNone(pagination_data.get("next"))
        else:
            self.assertIsNone(pagination_data.get("next"))

        if has_prev:
            self.assertIsNotNone(pagination_data.get("previous"))
        else:
            self.assertIsNone(pagination_data.get("previous"))
