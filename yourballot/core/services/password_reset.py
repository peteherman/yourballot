from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from rest_framework.request import Request

from yourballot.api.serializers.core.password_reset import PasswordResetRequestSerializer
from yourballot.core.auth.user import get_user_from_email
from yourballot.core.models.password_reset import PasswordReset


class PasswordResetService:

    @classmethod
    def create_password_reset(cls, request: Request) -> tuple[bool, str | None]:
        serializer = PasswordResetRequestSerializer(request)
        if not serializer.is_valid():
            return False, ", ".join(serializer.errors)

        email = serializer.validated_data.get("email")
        user = get_user_from_email(email)
        if not user:
            return False, "Unable to find a user with that email address"

        password_reset_code = cls.generate_secure_password_reset_code()
        password_reset: PasswordReset | None = None
        with transaction.atomic():
            cls.invalidate_existing_password_resets(user)
            password_reset = cls.create_password_reset_model(user, password_reset_code)

        cls.send_password_reset_email(password_reset)
        return True, None

    @classmethod
    def generate_secure_password_reset_code(cls) -> str:
        raise NotImplementedError("Need way to generate secure reset code")

    @classmethod
    def invalidate_existing_password_resets(cls, user: User) -> None:
        PasswordReset.objects.filter(user=user).update(invalidated=timezone.now())

    @classmethod
    def send_password_reset_email(cls, password_reset: PasswordReset) -> None:
        raise NotImplementedError("Need to implement email sending")

    @classmethod
    def create_password_reset_model(
        cls, user: User, password_reset_code: str
    ) -> PasswordReset:
        password_reset = PasswordReset.objects.create(
            user=user, reset_code=password_reset_code, invalidated=None
        )
        return password_reset
