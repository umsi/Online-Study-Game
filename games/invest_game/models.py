from django.db import models
from django.utils import timezone

from games.core.models import GamesUser, TimeStampedModel


class InvestmentGameUser(GamesUser):
    pass


class Investment(TimeStampedModel):
    # Valid experiment stage options
    STAGE_SELECT_RESPONDENT = "select_respondent"
    STAGE_USER_INVESTMENT = "user_investment"
    STAGE_RESPONDENT_INVESTMENT = "respondent_investment"
    STAGE_QUESTION_1 = "question1"
    STAGE_QUESTION_1_5 = "question1_5"
    STAGE_QUESTION_2 = "question2"
    STAGE_QUESTION_3 = "question3"
    STAGE_COMPARE = "compare"
    STAGE_FINISH = "finish"
    STAGE_CHOICES = (
        (STAGE_SELECT_RESPONDENT, "User reached respondent selection stage"),
        (STAGE_USER_INVESTMENT, "User reached user investment stage"),
        (STAGE_RESPONDENT_INVESTMENT, "User reached respondent investment stage"),
        (STAGE_QUESTION_1, "User reached question 1 stage"),
        (STAGE_QUESTION_1_5, "User reached question 1.5 stage"),
        (STAGE_QUESTION_2, "User reached question 2 stage"),
        (STAGE_QUESTION_3, "User reached question 3 stage"),
        (STAGE_COMPARE, "User reached compare stage"),
        (STAGE_FINISH, "User reached finish stage"),
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
        (RESPONDENT_IBRAHIM, "Respondent is Ibrahim"),
        (RESPONDENT_SAHR, "Respondent is Sahr"),
        (RESPONDENT_SAHAL, "Respondent is Sahal"),
        (RESPONDENT_OMAR, "Respondent is Omar"),
        (RESPONDENT_EMAN, "Respondent is Eman"),
        (RESPONDENT_DOUGLAS, "Respondent is Douglas"),
        (RESPONDENT_CHRISTOPHER, "Respondent is Christopher"),
        (RESPONDENT_PHILIP, "Respondent is Philip"),
        (RESPONDENT_THERESA, "Respondent is Theresa"),
        (RESPONDENT_TRACY, "Respondent is Tracy"),
    )

    # Valid multiple agreement question types
    MULTIPLE_AGREEMENT_CONTROL = "control"
    MULTIPLE_AGREEMENT_WITH_IMMIGRATION = "with_immigration"
    MULTIPLE_AGREEMENT_WITH_MUSLIM_IMMIGRATION = "with_muslim_immigration"
    MULTIPLE_AGREEMENT_CHOICES = (
        (MULTIPLE_AGREEMENT_CONTROL, "User was presented with the control question"),
        (
            MULTIPLE_AGREEMENT_WITH_IMMIGRATION,
            "User was presented with the immigration option",
        ),
        (
            MULTIPLE_AGREEMENT_WITH_MUSLIM_IMMIGRATION,
            "User was presented with the Muslim immigration option",
        ),
    )

    # Valid user bonus choices
    USER_BONUS = 2
    NO_USER_BONUS = 0
    USER_BONUS_CHOICES = (
        (USER_BONUS, "User received a bonus of $%s" % USER_BONUS),
        (NO_USER_BONUS, "User received no bonus ($0)"),
    )

    user = models.OneToOneField(
        InvestmentGameUser, on_delete=models.CASCADE, primary_key=True
    )
    reached_stage = models.CharField(
        max_length=256, choices=STAGE_CHOICES, default=STAGE_SELECT_RESPONDENT,
    )
    respondent = models.CharField(
        max_length=256, choices=RESPONDENT_CHOICES, default=None, null=True
    )
    user_investment = models.IntegerField(null=True)
    respondent_investment_guess = models.IntegerField(null=True)
    respondent_investment = models.IntegerField(null=True)
    user_bonus = models.IntegerField(choices=USER_BONUS_CHOICES, default=NO_USER_BONUS)
    user_received = models.IntegerField(null=True)

    started_user_investment = models.DateTimeField(null=True)
    finished_user_investment = models.DateTimeField(null=True)
    started_respondent_investment = models.DateTimeField(null=True)
    finished_respondent_investment = models.DateTimeField(null=True)

    us_citizen = models.CharField(max_length=255, null=True)
    voted_last_election = models.CharField(max_length=255, null=True)
    how_voted = models.CharField(max_length=255, null=True)
    political_views = models.CharField(max_length=255, null=True)
    multiple_agreement_question = models.CharField(max_length=255, null=True)
    multiple_agreement_question_type = models.CharField(
        max_length=255, choices=MULTIPLE_AGREEMENT_CHOICES, null=True
    )
    news_source = models.CharField(max_length=255, null=True)
    muslims_in_neighborhood = models.CharField(max_length=255, null=True)
    muslim_coworkers = models.CharField(max_length=255, null=True)
    self_treated_unfairly = models.CharField(max_length=255, null=True)
    race_treated_unfairly = models.CharField(max_length=255, null=True)
    religion_treated_unfairly = models.CharField(max_length=255, null=True)
    general_trustworthiness = models.CharField(max_length=255, null=True)
    economic_outlook = models.CharField(max_length=255, null=True)
    islamic_extremism = models.CharField(max_length=255, null=True)
    reducing_terrorism = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user.username
