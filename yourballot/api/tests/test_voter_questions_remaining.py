from rest_framework import status

from yourballot.api.tests.core import APITestCase
from yourballot.issue.models.factories.issue_question import IssueQuestionFactory
from yourballot.issue.models.factories.voter_issue_question_opinion import VoterIssueQuestionOpinionFactory
from yourballot.voter.models.factories.voter import VoterFactory


class TestVoterQuestionsRemaining(APITestCase):
    """
    Test cases for the /v1/voter/questions.remaining route
    """

    def test_no_values_when_no_questions_exist(self) -> None:
        response = self.client.get("/v1/voter/questions.remaining/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json())

    def test_one_question_when_one_question_exists_not_answered(self) -> None:
        question = IssueQuestionFactory.create()
        response = self.client.get("/v1/voter/questions.remaining/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json())

        results = response.json().get("result", [])

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], question.id)

    def test_no_question_when_voter_answered_question(self) -> None:
        question = IssueQuestionFactory.create()
        test_user_id = self.client.session["_auth_user_id"]
        voter = VoterFactory.create(user=test_user_id)

        VoterIssueQuestionOpinionFactory.create(voter=voter, issue_question=question, rating=5.0)
        response = self.client.get("/v1/voter/questions.remaining/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json())
