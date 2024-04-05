from django.contrib import admin

from yourballot.issue.models import CandidateIssueQuestionOpinion, Issue, IssueQuestion

admin.site.register(Issue)
admin.site.register(IssueQuestion)
admin.site.register(CandidateIssueQuestionOpinion)
