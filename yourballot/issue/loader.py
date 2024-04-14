from yourballot.issue.models.issue import Issue, IssueCategory
from yourballot.issue.models.issue_question import IssueQuestion
from yourballot.party.tendency import PoliticalTendency


def load_issues() -> None:
    """
    Initialize some issues within the database
    """
    issues = [
        Issue(
            name="Healthcare",
            category=IssueCategory.SOCIAL,
            low_score_tendency=PoliticalTendency.RIGHT,
            high_score_tendency=PoliticalTendency.LEFT,
        ),
        Issue(
            name="Abortion",
            category=IssueCategory.SOCIAL,
            low_score_tendency=PoliticalTendency.LEFT,
            high_score_tendency=PoliticalTendency.RIGHT,
        ),
        Issue(
            name="Gun Control",
            category=IssueCategory.SOCIAL,
            low_score_tendency=PoliticalTendency.LEFT,
            high_score_tendency=PoliticalTendency.RIGHT,
        ),
        Issue(
            name="Environment",
            category=IssueCategory.SOCIAL,
            low_score_tendency=PoliticalTendency.RIGHT,
            high_score_tendency=PoliticalTendency.RIGHT,
        ),
        Issue(
            name="Immigration",
            category=IssueCategory.SOCIAL,
            low_score_tendency=PoliticalTendency.LEFT,
            high_score_tendency=PoliticalTendency.RIGHT,
        ),
    ]
    Issue.objects.bulk_create(issues)


def load_questions() -> None:
    """
    Initialize a base question set within the database
    """
    if Issue.objects.count() <= 0:
        load_issues()

    issue_questions = []

    healthcare_issue = Issue.objects.get(name="Healthcare")
    issue_questions.extend(
        [
            IssueQuestion(
                name="Healthcare is a human right",
                question="Healthcare is a human right and no person should need to pay for healthcare",
                issue=healthcare_issue,
            ),
            IssueQuestion(
                name="Fed Gov't should ensure healthcare coverage",
                question="The federal government should be responsible for ensuring all American shave healthcare coverage",
                issue=healthcare_issue,
            ),
        ]
    )

    abortion_issue = Issue.objects.get(name="Abortion")
    issue_questions.extend(
        [
            IssueQuestion(
                name="All Abortion is murder",
                question="All abortion should be viewed as murder and it should be outlawed",
                issue=abortion_issue,
            ),
            IssueQuestion(
                name="No abortions after week 8",
                question="Abortions which occur after week 8 of pregnancy should be outlawed, regardless of the circumstances",
                issue=abortion_issue,
            ),
        ]
    )

    gun_control_issue = Issue.objects.get(name="Gun Control")
    issue_questions.extend(
        [
            IssueQuestion(
                name="No waiting period for gun purchase",
                question="There should not be a waiting period to purchase a gun",
                issue=gun_control_issue,
            ),
            IssueQuestion(
                name="No restrictions on ammo purchase",
                question="There should not be any restriction with respect to the amount of ammo a single individual can purchase at a time",
                issue=gun_control_issue,
            ),
        ]
    )

    environment_issue = Issue.objects.get(name="Environment")
    issue_questions.extend(
        [
            IssueQuestion(
                name="No gas vehicles after 2035",
                question="The government should prohibit the production of gas powered vehicles after the year 2035",
                issue=environment_issue,
            ),
            IssueQuestion(
                name="Fed Gov't not doing enough to stop climate change",
                question="The federal government is not doing enough to reduce the effects of climate change",
                issue=environment_issue,
            ),
        ]
    )

    immigration_issue = Issue.objects.get(name="Immigration")
    issue_questions.extend(
        [
            IssueQuestion(
                name="Close border for short period of time",
                question="The federal government should close the border, at least for a short period of time so that the individuals currently in the system can be processed",
                issue=immigration_issue,
            ),
            IssueQuestion(
                name="Restrict border",
                question="The federal government should more heavily restrict who is allowed through the border",
                issue=immigration_issue,
            ),
        ]
    )

    IssueQuestion.objects.bulk_create(issue_questions)
