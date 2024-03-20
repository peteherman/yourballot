from factory.django import DjangoModelFactory

from yourballot.issue.models.issue_question import VoterIssueQuestionOpinion


class VoterIssueQuestionOpinionFactory(DjangoModelFactory):

    class Meta:
        model = VoterIssueQuestionOpinion
