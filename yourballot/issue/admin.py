from django.contrib import admin

from yourballot.issue.models import CandidateIssueQuestionOpinion, Issue, IssueQuestion, VoterIssueQuestionOpinion

admin.site.register(Issue)
admin.site.register(IssueQuestion)
admin.site.register(CandidateIssueQuestionOpinion)
admin.site.register(VoterIssueQuestionOpinion)
