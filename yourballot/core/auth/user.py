from django.contrib.auth.models import User


def get_user_from_email(email: str) -> User | None:
    return User.objects.filter(email__iexact=email).first()
