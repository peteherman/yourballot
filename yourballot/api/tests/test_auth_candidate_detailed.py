from rest_framework import status

from yourballot.api.tests.core import APITestCase
from yourballot.candidate.models.candidate import Candidate
from yourballot.candidate.models.factories.candidate import CandidateFactory
from yourballot.issue.models.factories.candidate_issue_question_opinion import CandidateIssueQuestionOpinionFactory

expected_result_structure = {
    "external_id": str,
    "name": str,
    "age": int,
    "bio": str,
    "start_date": str | None,
    "ethnicity": str | None,
    "gender": str | None,
    "political_identity": str,
    "political_party": str,
    "position": {
        "id": int,
        "term_limit": int | None,
        "title": str,
        "locality": {
            "id": int,
            "name": str | None,
            "type": str | None,
            "updated": str | None,
            "geo_json_id": str | None,
            "created": str | None,
        },
    },
    "url": str | None,
    "twitter": str | None,
    "facebook": str | None,
    "profile_photo": str | None,
    "similarity": float,
    "issue_views": dict,
}


class TestAuthenticatedCandidateDetailView(APITestCase):
    """
    API Test cases for the /v1/candidate/{candidate_id} endpoint
    """

    def test_view_when_candidate_has_not_answered_questions(self) -> None:
        """
        Test view when neither voter nor candidate has answered a question
        """
        candidate = CandidateFactory.create()

        url = f"/v1/candidate/{candidate.id}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recursive_validate_result_structure(expected_result_structure, response.json())

    def test_view_when_candidate_has_answered_questions(self) -> None:
        candidate = CandidateFactory.create()
        num_questions = 10
        for _ in range(num_questions):
            CandidateIssueQuestionOpinionFactory.create(candidate=candidate)

        url = f"/v1/candidate/{candidate.id}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recursive_validate_result_structure(expected_result_structure, response.json())
