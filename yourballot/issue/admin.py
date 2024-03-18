from django.contrib import admin

from yourballot.issue.models import Issue, IssueQuestion

admin.site.register(Issue)
admin.site.register(IssueQuestion)
