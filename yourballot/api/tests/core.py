from types import UnionType
from typing import Any, cast

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from yourballot.voter.models.factories.voter import VoterFactory


class APITestCase(TestCase):

    def setUp(self) -> None:
        self.user, _ = User.objects.get_or_create(username="test-user")
        self.voter = VoterFactory.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
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

    def _assert_value_conforms_to_union_type(self, union_type: UnionType, actual: Any) -> None:
        self.assertTrue(any(isinstance(actual, t) for t in union_type.__args__))

    def recursive_validate_result_structure(self, expected_structure: Any, actual: Any) -> None:
        """
        Recursively traverses the expected structure and ensure the same structure and typing applies to :param: actual
        """
        if type(expected_structure) is UnionType:
            self._assert_value_conforms_to_union_type(expected_structure, actual)
            return

        if type(expected_structure) is type:
            self.assertIsInstance(
                actual, expected_structure, f"Expected structure: {expected_structure}, actual: {actual}"
            )
            return

        self.assertIsInstance(expected_structure, dict, f"Expected structure: {expected_structure}, actual: {actual}")
        self.assertIsInstance(actual, dict)
        self.assertSequenceEqual(sorted(expected_structure.keys()), sorted(actual.keys()))
        for key, substructure in expected_structure.items():
            self.assertTrue(key in actual, f"Expected Structure is a dict. Expected key: {key} in actual: {actual}")
            self.recursive_validate_result_structure(substructure, actual[key])
