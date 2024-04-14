from django.test import TestCase

from yourballot.issue.loader import load_questions


class TestGuestGetMatches(TestCase):

    def setUp(self) -> None:
        load_questions()

