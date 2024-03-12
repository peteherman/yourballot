from django.db import models
from django.utils.translation import gettext_lazy as _


class PoliticalTendency(models.TextChoices):
    LEFT = "LEFT", _("Left")
    RIGHT = "RIGHT", _("Right")
