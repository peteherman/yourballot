from typing import cast

from factory import Sequence
from factory.django import DjangoModelFactory

from yourballot.issue.models.issue import Issue


class IssueFactory(DjangoModelFactory):
    name: str = cast(str, Sequence(lambda n: f"Issue {n}"))

    class Meta:
        model = Issue
