from rest_framework import routers

from yourballot.api.views.questions.all_questions import AllQuestionsViewSet
from yourballot.api.views.voter.questions import VoterQuestionRemainingViewSet

all_question_router = routers.SimpleRouter()
all_question_router.register(r"questions", AllQuestionsViewSet)

voter_question_router = routers.SimpleRouter()
voter_question_router.register(r"questions\.remaining", VoterQuestionRemainingViewSet)
