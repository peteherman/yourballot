from rest_framework import routers

from yourballot.api.views.candidate.candidate import CandidateViewSet
from yourballot.api.views.guest.matches import GuestMatchViewSet
from yourballot.api.views.questions.all_questions import AllQuestionsViewSet
from yourballot.api.views.voter.answer_question import VoterAnswerQuestionViewSet
from yourballot.api.views.voter.candidates import VoterCandidateViewSet
from yourballot.api.views.voter.opinions import VoterOpinionViewSet
from yourballot.api.views.voter.questions import VoterQuestionRemainingViewSet

all_question_router = routers.SimpleRouter()
all_question_router.register(r"questions", AllQuestionsViewSet)

voter_question_router = routers.SimpleRouter()
voter_question_router.register(r"questions\.remaining", VoterQuestionRemainingViewSet)
voter_question_router.register(r"questions", VoterAnswerQuestionViewSet)

voter_opinions_router = routers.SimpleRouter()
voter_opinions_router.register(r"", VoterOpinionViewSet)
voter_candidate_router = routers.SimpleRouter()
voter_candidate_router.register(r"candidate", VoterCandidateViewSet)

candidate_router = routers.SimpleRouter()
candidate_router.register(r"", CandidateViewSet)

guest_match_router = routers.SimpleRouter()
guest_match_router.register(r"", GuestMatchViewSet)
