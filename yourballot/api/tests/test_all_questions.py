from rest_framework import status

from yourballot.api.tests.core import APITestCase
from yourballot.issue.models.factories.issue_question import IssueQuestionFactory
from yourballot.issue.models.issue_question import IssueQuestion


class TestIssueQuestion(APITestCase):
    """
    API Test cases for the /v1/questions/ route
    """

    def test_no_values_returned_when_no_questions_exist(self) -> None:
        """
        Test response is an empty list when no questions exist
        """
        response = self.client.get("v1/questions", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
