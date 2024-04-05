from django.contrib import admin

# Register your models here.
from yourballot.candidate.models.candidate import Candidate
from yourballot.candidate.models.candidate_position import CandidatePosition

admin.site.register(Candidate)
admin.site.register(CandidatePosition)
