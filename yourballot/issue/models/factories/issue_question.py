from factory.django import DjangoModelFactory

from yourballot.issue.models.issue_question import IssueQuestion


class IssueQuestionFactory(DjangoModelFactory):
    class Meta:
        model = IssueQuestion
