from django.contrib import admin

# Register your models here.
from yourballot.voter.models import Voter

admin.site.register(Voter)
