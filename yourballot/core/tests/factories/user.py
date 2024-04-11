from typing import cast

from django.contrib.auth.models import User
from factory import Sequence
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    username: str = cast(str, Sequence(lambda n: f"user_{n}"))

    class Meta:
        model = User
