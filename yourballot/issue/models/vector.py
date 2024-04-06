from django.db.models import Avg

from yourballot.candidate.models import Candidate
from yourballot.issue.models.issue import Issue
from yourballot.issue.models.issue_question import CandidateIssueQuestionOpinion, VoterIssue, VoterIssueQuestionOpinion
from yourballot.similarity.similarity import euclidean_distance
from yourballot.voter.models import Voter

max_rating: float = 10.0

ProfileVector = tuple[float, ...]


def calculate_voter_profile_vector(voter: Voter) -> ProfileVector:
    all_issues = Issue.objects.all()
    issue_map: dict[int, float] = {}
    for issue in all_issues:
        issue_map[issue.id] = 0.0

    voter_avg_issue_opinion = (
        VoterIssueQuestionOpinion.objects.values("issue_question__issue")
        .annotate(avg_rating=Avg("rating"))
        .values_list("issue_question__issue", "avg_rating", named=True)
    )
    for issue_rating in voter_avg_issue_opinion:
        issue_map[issue_rating.issue_question__issue] = issue_rating.avg_rating

    for issue_weight in VoterIssue.objects.filter(voter):
        issue_map[issue_weight.issue.id] *= issue_weight.weight

    return tuple([issue_map[key] for key in sorted(issue_map.keys())])


def calculate_candidate_profile_vector(candidate: Candidate) -> ProfileVector:
    all_issues = Issue.objects.all()
    issue_map: dict[int, float] = {}
    for issue in all_issues:
        issue_map[issue.id] = 0.0

    candidate_avg_issue_opinion = (
        CandidateIssueQuestionOpinion.objects.values("issue_question__issue")
        .annotate(avg_rating=Avg("rating"))
        .values_list("issue_question__issue", "avg_rating", named=True)
    )
    for issue_rating in candidate_avg_issue_opinion:
        issue_map[issue_rating.issue_question__issue] = issue_rating.avg_rating

    # TODO: perform weighting?

    return tuple([issue_map[key] for key in sorted(issue_map.keys())])


def calculate_vector_similarity(vector_a: ProfileVector, vector_b: ProfileVector) -> float:
    dist = euclidean_distance(vector_a, vector_b)
    return 1 - (dist / 1.0)


def max_euclidean_distance() -> float:
    max_vector_fields = Issue.objects.count()
    max_vector = tuple([max_rating for _ in range(max_vector_fields)])
    min_vector = tuple([-max_rating for _ in range(max_vector_fields)])
    return euclidean_distance(max_vector, min_vector)
