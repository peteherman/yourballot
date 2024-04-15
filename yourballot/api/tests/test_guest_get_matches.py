from random import uniform
from typing import Any

from rest_framework import status

from yourballot.api.tests.core import APITestCase
from yourballot.candidate.models.candidate import Candidate
from yourballot.candidate.models.factories.candidate import CandidateFactory
from yourballot.issue.loader import load_questions
from yourballot.issue.models.issue import Issue
from yourballot.locality.models.factories.zipcode_locality import ZipcodeLocalityFactory


class TestGuestGetMatches(APITestCase):
    url = "/v1/guest/candidates/"

    def setUp(self) -> None:
        load_questions()

    def generate_request_body(self, zipcode: str = "11111") -> dict[str, Any]:
        request_body = {"zipcode": zipcode, "issue_views": dict()}
        issues = Issue.objects.all()
        for issue in issues:
            request_body["issue_views"][issue.name] = uniform(-10.0, 10.0)  # type: ignore

        return request_body

    def test_no_candidates_no_matches(self) -> None:
        """
        Test no response when no candidates exist at all
        """

        request_body = self.generate_request_body()
        response = self.client.post(self.url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json(), total=0)

    def test_no_candidates_when_provided_zip_doesnt_match(self) -> None:
        """
        Test no results in response when no candidates exist in the provided zipcode
        """
        CandidateFactory.create_batch(size=100)

        # No matching zipcode localities exist so response should be none
        request_body = self.generate_request_body()
        response = self.client.post(self.url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json(), total=0)

    def test_single_candidate_match(self) -> None:
        zipcode = "12345"
        matching_zip_locality = ZipcodeLocalityFactory.create(zipcode=zipcode)

        candidate = CandidateFactory.create(position__locality=matching_zip_locality.political_locality)

        request_body = self.generate_request_body()
        request_body["zipcode"] = zipcode

        response = self.client.post(self.url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json(), total=1)
        self.assertEqual(response.json().get("result")[0]["id"], candidate.id)

    def test_multiple_candidate_match(self) -> None:
        zipcode = "12345"
        matching_zip_locality = ZipcodeLocalityFactory.create(zipcode=zipcode)

        num_matching_candidates = 100
        CandidateFactory.create_batch(
            size=num_matching_candidates, position__locality=matching_zip_locality.political_locality
        )

        request_body = self.generate_request_body()
        request_body["zipcode"] = zipcode

        response = self.client.post(self.url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json(), total=num_matching_candidates)

        ids_from_response = [entry["id"] for entry in response.json().get("result", [])]
        sorted_candidate_ids = [c.id for c in Candidate.objects.all().order_by("id")]

        self.assertSequenceEqual(ids_from_response, sorted_candidate_ids)
