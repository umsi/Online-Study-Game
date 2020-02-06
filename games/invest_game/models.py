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
        (RESPONDENT_IBRAHIM, "Your respondent is Ibrahim"),
        (RESPONDENT_SAHR, "Your respondent is Sahr"),
        (RESPONDENT_SAHAL, "Your respondent is Sahal"),
        (RESPONDENT_OMAR, "Your respondent is Omar"),
        (RESPONDENT_EMAN, "Your respondent is Eman"),
        (RESPONDENT_DOUGLAS, "Your respondent is Douglas"),
        (RESPONDENT_CHRISTOPHER, "Your respondent is Christopher"),
        (RESPONDENT_PHILIP, "Your respondent is Philip"),
        (RESPONDENT_THERESA, "Your respondent is Theresa"),
        (RESPONDENT_TRACY, "Your respondent is Tracy"),
    )

    user = models.OneToOneField(
        InvestmentGameUser, on_delete=models.CASCADE, primary_key=True
    )
    reached_stage = models.CharField(
        max_length=256, choices=STAGE_CHOICES, default=None, null=True,
    )
    respondent = models.CharField(
        max_length=256, choices=RESPONDENT_CHOICES, default=None, null=True
    )
    user_investment = models.IntegerField(null=True)
    respondent_investment_guess = models.IntegerField(null=True)
    respondent_investment = models.IntegerField(null=True)
    user_received = models.IntegerField(null=True)
    user_bonus = models.IntegerField(default=0)

    otherreturned = models.IntegerField(default=-1)
    otherinvested = models.IntegerField(default=-1)
    points = models.IntegerField(default=-1)

    started_user_investment = models.DateTimeField(null=True)
    finished_user_investment = models.DateTimeField(null=True)
    started_respondent_investment = models.DateTimeField(null=True)
    finished_respondent_investment = models.DateTimeField(null=True)

    q1answer = models.CharField(max_length=255, null=True)
    q2answer = models.CharField(max_length=255, null=True)
    q3answer = models.CharField(max_length=255, null=True)
    q4answer = models.CharField(max_length=255, null=True)
    q5answer = models.CharField(max_length=255, null=True)
    q6answer = models.CharField(max_length=255, null=True)
    q7answer = models.CharField(max_length=255, null=True)
    q8answer = models.CharField(max_length=255, null=True)
    q9answer = models.CharField(max_length=255, null=True)
    q10answer = models.CharField(max_length=255, null=True)
    q11answer = models.CharField(max_length=255, null=True)
    q12answer = models.CharField(max_length=255, null=True)
    q13answer = models.CharField(max_length=255, null=True)
    q14answer = models.CharField(max_length=255, null=True)
    q15answer = models.CharField(max_length=255, null=True)
    q5type = models.IntegerField(default=-1)

    def __str__(self):
        return self.user.username
