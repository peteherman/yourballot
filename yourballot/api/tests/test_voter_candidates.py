from rest_framework import status

from yourballot.api.tests.core import APITestCase
from yourballot.candidate.models.factories.candidate import CandidateFactory
from yourballot.locality.models.factories.political_locality import PoliticalLocalityFactory
from yourballot.locality.models.factories.zipcode_locality import ZipcodeLocalityFactory
from yourballot.voter.models.factories.voter import VoterFactory


class TestVoterCandidatesView(APITestCase):

    endpoint: str = "/v1/voter/candidate/"

    def test_empty_results_when_no_candidates_exist(self) -> None:
        """
        Test that fetching endpoint when no candidates exists results in an empty list
        """
        response = self.client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json(), total=0)

    def test_empty_results_when_no_candidate_in_voter_localities(self) -> None:
        """
        Tests that fetching endpoint when no candidates exist within a voters localities results in an empty list
        """
        candidate_political_locality = PoliticalLocalityFactory.create()
        candidate = CandidateFactory.create(position__locality=candidate_political_locality)

        voter_political_locality = PoliticalLocalityFactory.create()
        voter_zip_locality = ZipcodeLocalityFactory.create(
            zipcode=self.voter.zipcode, political_locality=voter_political_locality
        )

        # sanity check
        self.assertNotEqual(candidate.position.locality, voter_zip_locality.political_locality)

        response = self.client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json(), total=0)

    def test_single_voter_locality_one_candidate_match(self) -> None:
        """
        Test there are multiple candidates (in differing localities) and one candidate exists within a voter's locality
        """
        # Create candidate with matching locality
        candidate_political_locality = PoliticalLocalityFactory.create()
        matching_candidate = CandidateFactory.create(position__locality=candidate_political_locality)
        voter_zip_locality = ZipcodeLocalityFactory.create(
            zipcode=self.voter.zipcode, political_locality=candidate_political_locality
        )

        # Create lots of other candidates with other localities
        CandidateFactory.create_batch(size=100)

        # Sanity Check
        self.assertEqual(matching_candidate.position.locality, voter_zip_locality.political_locality)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json(), total=1)

    def test_single_voter_multiple_candidate_matches(self) -> None:
        """
        Test there are multiple candidates (in differing localities) and many candidates exist within a voter's locality
        """
        # Create candidate with matching locality
        candidate_political_locality = PoliticalLocalityFactory.create()
        num_expected_candidates = 100
        matching_candidates = CandidateFactory.create_batch(
            size=num_expected_candidates, position__locality=candidate_political_locality
        )

        voter_zip_locality = ZipcodeLocalityFactory.create(
            zipcode=self.voter.zipcode, political_locality=candidate_political_locality
        )

        # Create lots of other candidates with other localities (which don't match)
        CandidateFactory.create_batch(size=100)

        # Sanity Check
        self.assertEqual(matching_candidates[0].position.locality, voter_zip_locality.political_locality)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json(), total=num_expected_candidates)

        matching_candidates.sort(key=lambda x: x.id)
        expected_candidate_ids = [x.id for x in matching_candidates]
        response_candidate_ids = [x["id"] for x in response.json().get("result", [])]

        self.assertSequenceEqual(expected_candidate_ids, response_candidate_ids)

    def test_multiple_voters_multiple_candidate_matches(self) -> None:
        """
        Test there are multiple candidates (in differing localities) and many candidates exist within some voter's locality
        """
        # Create candidate with matching locality
        candidate_political_locality = PoliticalLocalityFactory.create()
        num_expected_candidates = 100
        matching_candidates = CandidateFactory.create_batch(
            size=num_expected_candidates, position__locality=candidate_political_locality
        )

        ZipcodeLocalityFactory.create(zipcode=self.voter.zipcode, political_locality=candidate_political_locality)

        other_voter_zip = "99999"
        VoterFactory.create(zipcode=other_voter_zip)
        other_locality = PoliticalLocalityFactory.create()
        ZipcodeLocalityFactory.create(zipcode=other_voter_zip, political_locality=other_locality)

        # Create lots of other candidates with other localities (which don't match)
        CandidateFactory.create_batch(size=100, position__locality=other_locality)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_pagination(response.json(), total=num_expected_candidates)

        matching_candidates.sort(key=lambda x: x.id)
        expected_candidate_ids = [x.id for x in matching_candidates]
        response_candidate_ids = [x["id"] for x in response.json().get("result", [])]

        self.assertSequenceEqual(expected_candidate_ids, response_candidate_ids)
