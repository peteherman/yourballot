from django.db.models import Avg
from numpy import array as np_array
from numpy.linalg import norm

from yourballot.candidate.models import Candidate
from yourballot.issue.models.issue import Issue
from yourballot.issue.models.issue_question import CandidateIssueQuestionOpinion, VoterIssue, VoterIssueQuestionOpinion
from yourballot.voter.models import Voter

max_rating: float = 10.0

ProfileVector = tuple[float, ...]


def euclidean_distance(vector_a: tuple[float, ...], vector_b: tuple[float, ...]) -> float:
    """
    Computes the euclidean distance between two vectors
    """
    assert len(vector_a) == len(vector_b)
    point_1 = np_array(vector_a)
    point_2 = np_array(vector_b)
    return float(norm(point_1 - point_2))


def calculate_voter_profile_vector(voter: Voter) -> ProfileVector:
    all_issues = Issue.objects.all()
    issue_map: dict[int, float] = {}
    for issue in all_issues:
        issue_map[issue.id] = 0.0

    voter_avg_issue_opinion = (
        VoterIssueQuestionOpinion.objects.filter(voter=voter)
        .values("issue_question__issue")
        .annotate(avg_rating=Avg("rating"))
        .values_list("issue_question__issue", "avg_rating", named=True)
    )
    for issue_rating in voter_avg_issue_opinion:
        issue_map[issue_rating.issue_question__issue] = issue_rating.avg_rating

    for issue_weight in VoterIssue.objects.filter(voter=voter):
        issue_map[issue_weight.issue.id] *= issue_weight.weight

    return tuple([issue_map[key] for key in sorted(issue_map.keys())])


def calculate_candidate_issue_views(candidate: Candidate) -> dict[str, float]:
    all_issues = Issue.objects.all()
    issue_map: dict[str, float] = {}
    for issue in all_issues:
        issue_map[issue.name] = 0.0

    candidate_avg_issue_opinion = (
        CandidateIssueQuestionOpinion.objects.filter(candidate=candidate)
        .values("issue_question__issue")
        .annotate(avg_rating=Avg("rating"))
        .values_list("issue_question__issue__name", "avg_rating", named=True)
    )
    for issue_rating in candidate_avg_issue_opinion:
        issue_map[issue_rating.issue_question__issue__name] = issue_rating.avg_rating

    return issue_map


def calculate_candidate_profile_vector(candidate: Candidate) -> ProfileVector:
    issue_map = calculate_candidate_issue_views(candidate)
    # TODO: perform weighting?
    return tuple([issue_map[key] for key in sorted(issue_map.keys())])


def calculate_vector_similarity(vector_a: ProfileVector, vector_b: ProfileVector) -> float:
    dist = euclidean_distance(vector_a, vector_b)
    return 1 - (dist / max_euclidean_distance())


def calculate_voter_candidate_similarity(voter: Voter, candidate: Candidate) -> float:
    voter_vector = calculate_voter_profile_vector(voter)
    candidate_vector = calculate_candidate_profile_vector(candidate)
    return calculate_vector_similarity(voter_vector, candidate_vector)


def convert_issue_views_dict_to_vector(issue_views: dict[str, float]) -> tuple[float, ...]:
    return tuple([issue_views[key] for key in sorted(issue_views.keys())])


def calculate_candidate_similarity_to_issue_views(candidate: Candidate, issue_views: dict[str, float]) -> float:
    guest_vector = convert_issue_views_dict_to_vector(issue_views)
    candidate_issue_views_map = calculate_candidate_issue_views(candidate)
    candidate_vector_of_issues_in_provided_issue_views = tuple(
        [candidate_issue_views_map.get(key, 0.0) for key in issue_views]
    )
    return calculate_vector_similarity(guest_vector, candidate_vector_of_issues_in_provided_issue_views)


def max_euclidean_distance() -> float:
    max_vector_fields = Issue.objects.count()
    max_vector = tuple([max_rating for _ in range(max_vector_fields)])
    min_vector = tuple([-max_rating for _ in range(max_vector_fields)])
    return max(euclidean_distance(max_vector, min_vector), 1.0)
