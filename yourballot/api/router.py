from rest_framework import routers

from yourballot.api.views.questions.all_questions import AllQuestionsViewSet

all_question_router = routers.SimpleRouter()
all_question_router.register(r"questions", AllQuestionsViewSet)
