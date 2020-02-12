from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser


class TimeStampedModel(models.Model):
    """
    Abstract base class providing auto-updating `created` and `updated`
    timestamps.
    """

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


class GamesUser(AbstractUser, TimeStampedModel):
    """
    Model representing a user participating in one or more games. It's intended
    that this model be subclassed by a User model for each game; e.g.
    InvestmentGameUser. That way game-specific fields can be added.
    """

    # TODO: This model might not be needed, but in case we need to track data
    # across multiple games (such as total earnings, etc.), this model would be
    # the place to store that data.

    def __str__(self):
        return self.username
