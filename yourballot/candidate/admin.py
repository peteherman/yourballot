from django.contrib import admin

# Register your models here.
from yourballot.candidate.models.candidate import Candidate

admin.site.register(Candidate)
