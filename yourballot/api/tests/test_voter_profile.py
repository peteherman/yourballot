from rest_framework import status

from yourballot.api.tests.core import APITestCase
from yourballot.candidate.models.factories.candidate import CandidateFactory
from yourballot.locality.models.factories.political_locality import \
    PoliticalLocalityFactory
from yourballot.locality.models.factories.zipcode_locality import ZipcodeLocalityFactory
from yourballot.voter.models.factories.voter import VoterFactory


class TestVoterProfileView(APITestCase):

    endpoint: str = "/v1/voter/profile/"

    def test_get(self) -> None:
        """
        Test fetching profile of default test user
        """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Response; ", response.json())
