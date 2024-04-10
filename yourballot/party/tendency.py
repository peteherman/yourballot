from django.db import models
from django.utils.translation import gettext_lazy as _


class PoliticalTendency(models.TextChoices):
    LEFT = "left", _("Left")
    RIGHT = "right", _("Right")
