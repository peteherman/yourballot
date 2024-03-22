from typing import cast

from rest_framework import status

from yourballot.api.tests.core import APITestCase
from yourballot.issue.models import VoterIssueQuestionOpinion
from yourballot.issue.models.factories.issue_question import IssueQuestionFactory, VoterIssueQuestionOpinionFactory


class TestVoterAnswerQuestions(APITestCase):
    """
    API Test cases for the /v1/voter/questions route
    """

    endpoint = "/v1/voter/questions/"

    def test_failure_when_no_issue_questions_exist(self) -> None:
        body = {
            "issue_question": 1231231231,
            "rating": 5.0,
        }

        response = self.client.post(self.endpoint, data=body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_when_rating_not_provided(self) -> None:
        question = IssueQuestionFactory.create()
        body = {
            "issue_question": question.id,
        }
        response = self.client.post(self.endpoint, data=body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_when_rating_is_negative(self) -> None:
        question = IssueQuestionFactory.create()
        body = {
            "issue_question": question.id,
            "rating": -1.0,
        }
        response = self.client.post(self.endpoint, data=body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_when_rating_is_too_high(self) -> None:
        question = IssueQuestionFactory.create()
        body = {
            "issue_question": question.id,
            "rating": 11.0,
        }
        response = self.client.post(self.endpoint, data=body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ok_when_question_exists_and_rating_within_bounds(self) -> None:
        self.assertEqual(VoterIssueQuestionOpinion.objects.count(), 0)
        question = IssueQuestionFactory.create()
        body = {
            "issue_question": question.id,
            "rating": 9.0,
        }
        response = self.client.post(self.endpoint, data=body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VoterIssueQuestionOpinion.objects.count(), 1)

    def test_old_answer_updated_when_answering_same_question_as_before(self) -> None:
        """
        Test that a new answer is not created, and instead an old is updated, when a voter reanswers a question
        """
        question = IssueQuestionFactory.create()
        old_rating = 3.0
        VoterIssueQuestionOpinionFactory.create(voter=self.voter, issue_question=question, rating=old_rating)
        self.assertEqual(VoterIssueQuestionOpinion.objects.count(), 1)

        new_rating = 5.0
        question = IssueQuestionFactory.create()
        body = {
            "issue_question": question.id,
            "rating": new_rating,
        }
        response = self.client.post(self.endpoint, data=body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VoterIssueQuestionOpinion.objects.count(), 1)
        question_response = VoterIssueQuestionOpinion.objects.first()
        self.assertIsNotNone(question_response)
        question_response = cast(VoterIssueQuestionOpinion, question_response)
        self.assertEqual(question_response.rating, new_rating)
