from typing import Any

from django.test import TestCase

from yourballot.api.serializers.voter.register import VoterRegistrationSerializer
from yourballot.party import PoliticalParty
from yourballot.voter.models.voter import Ethnicity, Gender, Race, Voter


class TestVoterRegistrationSerializer(TestCase):
    serializer_class = VoterRegistrationSerializer

    def test_email(self) -> None:
        test_cases: list[dict[str, Any]] = [
            {
                "name": "'email' not in body",
                "valid": False,
            },
            {
                "name": "email is None",
                "email": None,
                "valid": False,
            },
            {
                "name": "email is blank",
                "email": "",
                "valid": False,
            },
            {
                "name": "email is invalid",
                "email": "invalid-email",
                "valid": False,
            },
            {
                "name": "email is valid",
                "email": "test@mail.com",
                "valid": True,
            },
        ]

        body = {
            "age": 21,
            "ethnicity": Ethnicity.HISPANIC_OR_LATINO,
            "gender": Gender.FEMALE,
            "race": Race.NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER,
            "political_identity": "Middle",
            "political_party": PoliticalParty.INDEPENDENT,
            "zipcode": "12831",
            "password": "Password",
        }

        for test_case in test_cases:
            if "email" in test_case:
                body["email"] = test_case["email"]

            serializer = self.serializer_class(data=body)
            self.assertEqual(test_case.get("valid"), serializer.is_valid(), f"{test_case.get('name')} failed!")

    def test_age(self) -> None:
        test_cases: list[dict[str, Any]] = [
            {
                "name": "'age' not in body",
                "valid": True,
            },
            {
                "name": "age is None",
                "age": None,
                "valid": True,
            },
            {
                "name": "age is invalid",
                "age": -1,
                "valid": False,
            },
            {
                "name": "age is valid",
                "age": 0,
                "valid": True,
            },
        ]

        body = {
            "email": "test@mail.com",
            "ethnicity": Ethnicity.HISPANIC_OR_LATINO,
            "gender": Gender.FEMALE,
            "race": Race.NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER,
            "political_identity": "Middle",
            "political_party": PoliticalParty.INDEPENDENT,
            "zipcode": "12831",
            "password": "Password",
        }

        for test_case in test_cases:
            if "age" in test_case:
                body["age"] = test_case["age"]

            serializer = self.serializer_class(data=body)
            self.assertEqual(test_case.get("valid"), serializer.is_valid(), f"{test_case.get('name')} failed!")

    def test_gender(self) -> None:
        test_cases: list[dict[str, Any]] = [
            {
                "name": "'gender' not in body",
                "valid": True,
            },
            {
                "name": "gender is None",
                "gender": None,
                "valid": True,
            },
            {
                "name": "gender is invalid",
                "gender": "some gender",
                "valid": False,
            },
            {
                "name": "gender is valid",
                "gender": Gender.FEMALE,
                "valid": True,
            },
        ]

        body = {
            "age": 1,
            "email": "test@mail.com",
            "ethnicity": Ethnicity.HISPANIC_OR_LATINO,
            "race": Race.NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER,
            "political_identity": "Middle",
            "political_party": PoliticalParty.INDEPENDENT,
            "zipcode": "12831",
            "password": "Password",
        }

        for test_case in test_cases:
            if "gender" in test_case:
                body["gender"] = test_case["gender"]

            serializer = self.serializer_class(data=body)
            self.assertEqual(test_case.get("valid"), serializer.is_valid(), f"{test_case.get('name')} failed!")

    def test_ethnicity(self) -> None:
        test_cases: list[dict[str, Any]] = [
            {
                "name": "'ethnicity' not in body",
                "valid": True,
            },
            {
                "name": "ethnicity is None",
                "ethnicity": None,
                "valid": True,
            },
            {
                "name": "ethnicity is invalid",
                "ethnicity": "some ethnicity",
                "valid": False,
            },
            {
                "name": "ethnicity is blank",
                "ethnicity": "",
                "valid": False,
            },
            {
                "name": "ethnicity is valid",
                "ethnicity": Ethnicity.HISPANIC_OR_LATINO,
                "valid": True,
            },
        ]

        body = {
            "age": 1,
            "email": "test@mail.com",
            "gender": Gender.OTHER,
            "race": Race.NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER,
            "political_identity": "Middle",
            "political_party": PoliticalParty.INDEPENDENT,
            "zipcode": "12831",
            "password": "Password",
        }

        for test_case in test_cases:
            if "ethnicity" in test_case:
                body["ethnicity"] = test_case["ethnicity"]

            serializer = self.serializer_class(data=body)
            self.assertEqual(test_case.get("valid"), serializer.is_valid(), f"{test_case.get('name')} failed!")

    def test_race(self) -> None:

        test_cases: list[dict[str, Any]] = [
            {
                "name": "'race' not in body",
                "valid": True,
            },
            {
                "name": "race is None",
                "race": None,
                "valid": True,
            },
            {
                "name": "race is invalid",
                "race": "some race",
                "valid": False,
            },
            {
                "name": "race is blank",
                "race": "",
                "valid": False,
            },
            {
                "name": "race is valid",
                "race": Race.NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER,
                "valid": True,
            },
        ]

        body = {
            "age": 1,
            "email": "test@mail.com",
            "gender": Gender.OTHER,
            "ethnicity": Ethnicity.HISPANIC_OR_LATINO,
            "political_identity": "Middle",
            "political_party": PoliticalParty.INDEPENDENT,
            "zipcode": "12831",
            "password": "Password",
        }

        for test_case in test_cases:
            if "race" in test_case:
                body["race"] = test_case["race"]

            serializer = self.serializer_class(data=body)
            self.assertEqual(test_case.get("valid"), serializer.is_valid(), f"{test_case.get('name')} failed!")

    def test_political_identity(self) -> None:
        test_cases: list[dict[str, Any]] = [
            {
                "name": "'political_identity' not in body",
                "valid": False,
            },
            {
                "name": "political_identity is None",
                "political_identity": None,
                "valid": False,
            },
            {
                "name": "political_identity is blank",
                "political_identity": "",
                "valid": True,
            },
            {
                "name": "political_identity is valid",
                "political_identity": "Middle",
                "valid": True,
            },
            {
                "name": "political_identity is too long",
                "political_identity": "Abc" * 1000,
                "valid": False,
            },
        ]

        body = {
            "age": 1,
            "email": "test@mail.com",
            "gender": Gender.OTHER,
            "ethnicity": Ethnicity.HISPANIC_OR_LATINO,
            "race": Race.NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER,
            "political_party": PoliticalParty.INDEPENDENT,
            "zipcode": "12831",
            "password": "Password",
        }

        for test_case in test_cases:
            if "political_identity" in test_case:
                body["political_identity"] = test_case["political_identity"]

            serializer = self.serializer_class(data=body)
            self.assertEqual(test_case.get("valid"), serializer.is_valid(), f"{test_case.get('name')} failed!")

    def test_political_party(self) -> None:
        test_cases: list[dict[str, Any]] = [
            {
                "name": "'political_party' not in body",
                "valid": True,
            },
            {
                "name": "political_party is None",
                "political_party": None,
                "valid": True,
            },
            {
                "name": "political_party is blank",
                "political_party": "",
                "valid": False,
            },
            {
                "name": "political_party is invalid",
                "political_party": "invalid party",
                "valid": False,
            },
            {
                "name": "political_party is valid",
                "political_party": PoliticalParty.INDEPENDENT,
                "valid": True,
            },
        ]

        body = {
            "age": 1,
            "email": "test@mail.com",
            "gender": Gender.OTHER,
            "ethnicity": Ethnicity.HISPANIC_OR_LATINO,
            "race": Race.NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER,
            "political_identity": "Middle",
            "zipcode": "12831",
            "password": "Password",
        }

        for test_case in test_cases:
            if "political_party" in test_case:
                body["political_party"] = test_case["political_party"]

            serializer = self.serializer_class(data=body)
            self.assertEqual(test_case.get("valid"), serializer.is_valid(), f"{test_case.get('name')} failed!")

    def test_zipcode(self) -> None:
        test_cases: list[dict[str, Any]] = [
            {
                "name": "'zipcode' not in body",
                "valid": True,
            },
            {
                "name": "zipcode is None",
                "zipcode": None,
                "valid": False,
            },
            {
                "name": "zipcode is blank",
                "zipcode": "",
                "valid": False,
            },
            {
                "name": "zipcode is invalid (has letters)",
                "zipcode": "abc",
                "valid": False,
            },
            {
                "name": "zipcode is invalid (too long)",
                "zipcode": "1" * 12,
                "valid": False,
            },
            {
                "name": "zipcode is invalid (too short)",
                "zipcode": "123",
                "valid": False,
            },
            {
                "name": "zipcode is valid",
                "zipcode": "12345",
                "valid": True,
            },
        ]

        body = {
            "age": 1,
            "email": "test@mail.com",
            "gender": Gender.OTHER,
            "ethnicity": Ethnicity.HISPANIC_OR_LATINO,
            "race": Race.NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER,
            "political_identity": "Middle",
            "zipcode": "12831",
            "password": "Password",
        }

        for test_case in test_cases:
            if "zipcode" in test_case:
                body["zipcode"] = test_case["zipcode"]

            serializer = self.serializer_class(data=body)
            self.assertEqual(test_case.get("valid"), serializer.is_valid(), f"{test_case.get('name')} failed!")

    def test_password(self) -> None:
        test_cases: list[dict[str, Any]] = [
            {
                "name": "'password' not in body",
                "valid": False,
            },
            {
                "name": "password is None",
                "password": None,
                "valid": False,
            },
            {
                "name": "password is blank",
                "password": "",
                "valid": False,
            },
            {
                "name": "password is invalid (too long)",
                "password": "1" * 300,
                "valid": False,
            },
            {
                "name": "password is invalid (too short)",
                "password": "123",
                "valid": False,
            },
            {
                "name": "password is valid",
                "password": "asbascda",
                "valid": True,
            },
        ]

        body = {
            "age": 1,
            "email": "test@mail.com",
            "gender": Gender.OTHER,
            "ethnicity": Ethnicity.HISPANIC_OR_LATINO,
            "race": Race.NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER,
            "political_identity": "Middle",
            "zipcode": "12831",
        }

        for test_case in test_cases:
            if "password" in test_case:
                body["password"] = test_case["password"]

            serializer = self.serializer_class(data=body)
            self.assertEqual(test_case.get("valid"), serializer.is_valid(), f"{test_case.get('name')} failed!")
