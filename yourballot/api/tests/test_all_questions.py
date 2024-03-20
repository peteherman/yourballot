from typing import cast

from django.conf import settings
from rest_framework import status

from yourballot.api.tests.core import APITestCase
from yourballot.issue.models.factories.issue_question import IssueQuestionFactory


class TestIssueQuestion(APITestCase):
    """
    API Test cases for the /v1/questions/ route
    """

    def test_no_values_returned_when_no_questions_exist(self) -> None:
        """
        Test response is an empty list when no questions exist
        """
        response = self.client.get("/v1/questions/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json())

    def test_single_value_returned_when_one_question_exists(self) -> None:
        IssueQuestionFactory.create()
        response = self.client.get("/v1/questions/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json(), total=1)

    def test_pagination_when_more_than_two_pages_exist(self) -> None:
        page_size = cast(int, settings.REST_FRAMEWORK.get("PAGE_SIZE", 100))
        total_num_questions = page_size * 3
        IssueQuestionFactory.create_batch(size=total_num_questions)
        response = self.client.get("/v1/questions/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json(), total=total_num_questions, has_next=True)

        next_page = response.json()["result_info"]["next"]
        response = self.client.get(next_page, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json(), total=total_num_questions, has_prev=True, has_next=True)

        last_page = response.json()["result_info"]["next"]
        response = self.client.get(last_page, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json(), total=total_num_questions, has_prev=True, has_next=False)
