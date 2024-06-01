from django.contrib import admin

# Register your models here.
from yourballot.core.models.password_reset import PasswordReset

admin.site.register(PasswordReset)
