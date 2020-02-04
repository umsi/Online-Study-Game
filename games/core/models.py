from django.db import models

from django.contrib.auth.models import AbstractUser


class TimeStampedModel(models.Model):
    """
    Abstract base class providing auto-updating `created` and `updated` fields.
    """
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    class Meta:
        abstract = True


class GamesUser(AbstractUser, TimeStampedModel):
    """
    Model representing a user participating in one or more games.
    """
    # version = models.CharField(max_length=13, default="")
    totalearning = models.FloatField(default=0)
    experimentearning = models.FloatField(default=0)
    # startedstudy = models.DateTimeField(default=timezone.now)
    # finishedstudy = models.DateTimeField(default=timezone.now)
    optout = models.BooleanField(default=0)
    postpone = models.BooleanField(default=0)
    # age = models.IntegerField(blank=True)
    # gender = models.CharField(max_length=127, blank=True)
    # q1answer = models.CharField(max_length=25, blank=True)
    # q2answer = models.CharField(max_length=25, blank=True)
    # q3answer = models.CharField(max_length=25, blank=True)
    # q4answer = models.CharField(max_length=25, blank=True)
    # ownpc = models.NullBooleanField()
    # ownsmartphone = models.NullBooleanField()
    # ownpda = models.NullBooleanField()
    # ownotherdevice = models.NullBooleanField()
    # otherdevice = models.CharField(max_length=255, blank=True)
    # internetuse = models.CharField(max_length=25, blank=True)
    # fullname = models.CharField(max_length=255, default="")
    # street = models.CharField(max_length=255, blank=True)
    # city = models.CharField(max_length=255, blank=True)
    # state = models.CharField(max_length=255, blank=True)
    # zipcode = models.CharField(max_length=255, blank=True)
    # yearsofeduction = models.CharField(max_length=127, blank=True)
    # ethnicity = models.CharField(max_length=127, blank=True)
    # maritalstatus = models.CharField(max_length=127, blank=True)

    def __str__(self):
        return self.username
