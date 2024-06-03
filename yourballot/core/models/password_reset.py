from django.contrib.auth.models import User
from django.db import models


class PasswordReset(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    reset_code = models.CharField(max_length=16, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    invalidated = models.DateTimeField(null=True, default=None)
