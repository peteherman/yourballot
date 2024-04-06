from django.contrib.auth.models import User
from django.db.models.fields import FloatField
from django.test import TestCase

from yourballot.issue.models.factories.candidate_vector import CandidateVectorFactory
from yourballot.issue.models.factories.voter_vector import VoterVectorFactory
from yourballot.issue.models.vector import BaseVector
from yourballot.similarity.similarity import euclidean_distance


class TestVectorSimilarity(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_model_conversion_to_vector(self) -> None:
        issue_map = {"immigration": 1.0, "environment": 3.0, "gun_control": 5.0}

        voter_vector_model = VoterVectorFactory.create(**issue_map, voter__user=self.user)
        candidate_vector_model = CandidateVectorFactory.create(**issue_map, candidate__user=self.user)

        expected_vector = tuple([issue_map[sorted_key] for sorted_key in sorted(issue_map.keys())])
        voter_actual_vector = voter_vector_model.convert_to_vector_tuple()
        voter_actual_vector_no_zeros = tuple([mag for mag in voter_actual_vector if mag != 0.0])
        candidate_actual_vector = candidate_vector_model.convert_to_vector_tuple()
        candidate_actual_vector_no_zeros = tuple([mag for mag in candidate_actual_vector if mag != 0.0])
        self.assertSequenceEqual(expected_vector, voter_actual_vector_no_zeros)
        self.assertSequenceEqual(expected_vector, candidate_actual_vector_no_zeros)
        self.assertSequenceEqual(voter_actual_vector, candidate_actual_vector)

    def test_euclidean_distances_with_known_values(self) -> None:
        self.assertEqual(34.641, round(euclidean_distance((-10.0, -10.0, -10.0), (10.0, 10.0, 10.0)), 3))
        self.assertEqual(0.0, round(euclidean_distance((10.0, 10.0, 10.0), (10.0, 10.0, 10.0)), 3))

    def test_similarity_scores_same_vector(self) -> None:
        issue_map = {"immigration": 1.0, "environment": 3.0, "gun_control": 5.0}

        voter_vector_model = VoterVectorFactory.create(**issue_map, voter__user=self.user)
        candidate_vector_model = CandidateVectorFactory.create(**issue_map, candidate__user=self.user)
        self.assertEqual(1, voter_vector_model.similarity(candidate_vector_model))

    def test_similarity_scores_opposite_vectors(self) -> None:

        issue_map = {}
        opposite_issue_map = {}
        for vector_field in BaseVector.vector_fields():
            issue_map[vector_field.name] = 10.0
            opposite_issue_map[vector_field.name] = -10.0

        voter_vector_model = VoterVectorFactory.create(**issue_map, voter__user=self.user)

        candidate_vector_model = CandidateVectorFactory.create(**opposite_issue_map, candidate__user=self.user)
        self.assertEqual(0.0, voter_vector_model.similarity(candidate_vector_model))
