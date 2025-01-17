from rest_framework import routers

from yourballot.api.views.candidate.candidate import CandidateViewSet
from yourballot.api.views.guest.matches import GuestMatchViewSet
from yourballot.api.views.guest.questions import GuestQuestionViewSet
from yourballot.api.views.questions.all_questions import AllQuestionsViewSet
from yourballot.api.views.voter.answer_question import VoterAnswerQuestionViewSet
from yourballot.api.views.voter.candidates import VoterCandidateViewSet
from yourballot.api.views.voter.login import VoterLoginViewSet
from yourballot.api.views.voter.opinions import VoterOpinionViewSet
from yourballot.api.views.voter.profile import VoterProfileViewSet
from yourballot.api.views.voter.questions import VoterQuestionRemainingViewSet
from yourballot.api.views.voter.register import VoterRegisterViewSet

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

guest_questions_router = routers.SimpleRouter()
guest_questions_router.register(r"", GuestQuestionViewSet)

voter_register_router = routers.SimpleRouter()
voter_register_router.register(r"", VoterRegisterViewSet)

voter_login_router = routers.SimpleRouter()
voter_login_router.register(r"", VoterLoginViewSet)

voter_profile_router = routers.SimpleRouter()
voter_profile_router.register(r"", VoterProfileViewSet)
