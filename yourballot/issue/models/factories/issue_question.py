from typing import cast

from factory import SubFactory
from factory.django import DjangoModelFactory

from yourballot.issue.models.factories.issue import IssueFactory
from yourballot.issue.models.issue import Issue
from yourballot.issue.models.issue_question import IssueQuestion


class IssueQuestionFactory(DjangoModelFactory):
    issue: Issue = cast(Issue, SubFactory(IssueFactory))

    class Meta:
        model = IssueQuestion
