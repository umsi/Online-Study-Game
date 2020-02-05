from django.db import models
from django.utils import timezone

from games.core.models import GamesUser, TimeStampedModel


class InvestmentGameUser(GamesUser):
    pass


class Investment(TimeStampedModel):
    # Valid experiment stage options
    SELECT_RESPONDENT = "select-respondent"
    USER_INVESTMENT = "user-investment"
    RESPONDENT_INVESTMENT = "respondent-invenstment"
    COMPARISON = "comparison"
    THANK_YOU = "thank-you"
    STAGE_CHOICES = (
        (SELECT_RESPONDENT, "Reached respondent selection stage"),
        (USER_INVESTMENT, "Reached user investment stage"),
        (RESPONDENT_INVESTMENT, "Reached respondent investment stage"),
        (COMPARISON, "Reached comparison stage"),
        (THANK_YOU, "Reached thank you stage"),
    )

    # Valid respondent options
    RESPONDENT_IBRAHIM = "Ibrahim"
    RESPONDENT_SAHR = "Sahr"
    RESPONDENT_SAHAL = "Sahal"
    RESPONDENT_OMAR = "Omar"
    RESPONDENT_EMAN = "Eman"
    RESPONDENT_DOUGLAS = "Douglas"
    RESPONDENT_CHRISTOPHER = "Christopher"
    RESPONDENT_PHILIP = "Philip"
    RESPONDENT_TRACY = "Tracy"
    RESPONDENT_THERESA = "Theresa"
    RESPONDENT_CHOICES = (
        (RESPONDENT_IBRAHIM, "Ibrahim"),
        (RESPONDENT_SAHR, "Sahr"),
        (RESPONDENT_SAHAL, "Sahal"),
        (RESPONDENT_OMAR, "Omar"),
        (RESPONDENT_EMAN, "Eman"),
        (RESPONDENT_DOUGLAS, "Douglas"),
        (RESPONDENT_CHRISTOPHER, "Christopher"),
        (RESPONDENT_PHILIP, "Philip"),
        (RESPONDENT_THERESA, "Theresa"),
        (RESPONDENT_TRACY, "Tracy"),
    )

    user = models.OneToOneField(
        InvestmentGameUser, on_delete=models.CASCADE, primary_key=True
    )
    reached_stage = models.CharField(
        max_length=256, choices=STAGE_CHOICES, default=None, null=True,
    )
    respondent = models.CharField(
        max_length=256, choices=RESPONDENT_CHOICES, null=True, blank=True
    )

    invested = models.IntegerField(default=-1)
    doneinvest = models.IntegerField(default=-1)
    donereturn = models.IntegerField(default=-1)
    returned0 = models.IntegerField(default=-1)
    returned1 = models.IntegerField(default=-1)
    returned2 = models.IntegerField(default=-1)
    returned3 = models.IntegerField(default=-1)
    returned4 = models.IntegerField(default=-1)
    returned5 = models.IntegerField(default=-1)
    otherreturned = models.IntegerField(default=-1)
    otherinvested = models.IntegerField(default=-1)
    points = models.IntegerField(default=-1)

    q1answer = models.CharField(max_length=255, default=" ")
    q2answer = models.CharField(max_length=255, default=" ")
    q3answer = models.CharField(max_length=255, default=" ")
    q4answer = models.CharField(max_length=255, default=" ")
    q5answer = models.CharField(max_length=255, default=" ")
    q6answer = models.CharField(max_length=255, default=" ")
    q7answer = models.CharField(max_length=255, default=" ")
    q8answer = models.CharField(max_length=255, default=" ")
    q9answer = models.CharField(max_length=255, default=" ")
    q10answer = models.CharField(max_length=255, default=" ")
    q11answer = models.CharField(max_length=255, default=" ")
    q12answer = models.CharField(max_length=255, default=" ")
    q13answer = models.CharField(max_length=255, default=" ")
    q14answer = models.CharField(max_length=255, default=" ")
    q15answer = models.CharField(max_length=255, default=" ")
    q5type = models.IntegerField(default=-1)
    startedinvested = models.DateTimeField(default=timezone.now)
    finishedinvested = models.DateTimeField(default=timezone.now)
    startedreturned0 = models.DateTimeField(default=timezone.now)
    finishedreturned0 = models.DateTimeField(default=timezone.now)
    startedreturned1 = models.DateTimeField(default=timezone.now)
    finishedreturned1 = models.DateTimeField(default=timezone.now)
    startedreturned2 = models.DateTimeField(default=timezone.now)
    finishedreturned2 = models.DateTimeField(default=timezone.now)
    startedreturned3 = models.DateTimeField(default=timezone.now)
    finishedreturned3 = models.DateTimeField(default=timezone.now)
    startedreturned4 = models.DateTimeField(default=timezone.now)
    finishedreturned4 = models.DateTimeField(default=timezone.now)
    startedreturned5 = models.DateTimeField(default=timezone.now)
    finishedreturned5 = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
