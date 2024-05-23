from django.contrib.auth.models import User
from rest_framework.request import Request

from yourballot.voter.exceptions import VoterCreationFailureException
from yourballot.voter.models.voter import Voter


class VoterService:

    @classmethod
    def create_voter(cls, request: Request) -> Voter:
        """
        Creates a django user and a Voter. Raises an exception if creating a voter fails
        """
        raise NotImplementedError
