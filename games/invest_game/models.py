from django.db import models
from django.utils import timezone

from games.core.models import GamesUser, TimeStampedModel


class InvestmentGameUser(GamesUser):
    pass


class Investment(TimeStampedModel):
    # Valid experiment stage options:
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

    # Valid respondent options:
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

    # Valid multiple agreement question types:
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

    # Valid user bonus choices:
    USER_BONUS = 2
    NO_USER_BONUS = 0
    USER_BONUS_CHOICES = (
        (USER_BONUS, "User received a bonus of $%s" % USER_BONUS),
        (NO_USER_BONUS, "User received no bonus ($0)"),
    )

    # TODO: Ideally all these choices should be used to derive the
    # questionnaire forms themselves, using Django's ModelForms. Currently
    # that's not the case--all form options are duplicated in templates.

    # Valid question1 choices:
    # ------------------------
    # Are you a U.S. citizen?
    QUESTION_PAGE_1_Q1_OPTION_A = "yes"
    QUESTION_PAGE_1_Q1_OPTION_B = "no"
    QUESTION_PAGE_1_Q1_OPTION_C = "dont_know"
    QUESTION_PAGE_1_Q1_OPTION_D = "refuse_to_answer"
    QUESTION_PAGE_1_Q1_CHOICES = (
        (QUESTION_PAGE_1_Q1_OPTION_A, "Yes"),
        (QUESTION_PAGE_1_Q1_OPTION_B, "No"),
        (QUESTION_PAGE_1_Q1_OPTION_C, "Don't know"),
        (QUESTION_PAGE_1_Q1_OPTION_D, "Refuse to answer"),
    )

    # Valid question1_5 choices:
    # --------------------------
    # Did you vote for a presidential candidate in the last election?
    QUESTION_PAGE_1_5_Q1_OPTION_A = "yes"
    QUESTION_PAGE_1_5_Q1_OPTION_B = "no"
    QUESTION_PAGE_1_5_Q1_OPTION_C = "dont_know"
    QUESTION_PAGE_1_5_Q1_OPTION_D = "refuse_to_answer"
    QUESTION_PAGE_1_5_Q1_CHOICES = (
        (QUESTION_PAGE_1_5_Q1_OPTION_A, "Yes"),
        (QUESTION_PAGE_1_5_Q1_OPTION_B, "No"),
        (QUESTION_PAGE_1_5_Q1_OPTION_C, "Don't know"),
        (QUESTION_PAGE_1_5_Q1_OPTION_D, "Refuse to answer"),
    )

    # Whom did you vote for?
    QUESTION_PAGE_1_5_Q2_OPTION_A = "trump"
    QUESTION_PAGE_1_5_Q2_OPTION_B = "clinton"
    QUESTION_PAGE_1_5_Q2_OPTION_C = "other"
    QUESTION_PAGE_1_5_Q2_OPTION_D = "dont_know"
    QUESTION_PAGE_1_5_Q2_OPTION_E = "refuse_to_answer"
    QUESTION_PAGE_1_5_Q2_CHOICES = (
        (QUESTION_PAGE_1_5_Q2_OPTION_A, "Donald Trump"),
        (QUESTION_PAGE_1_5_Q2_OPTION_B, "Hillary Clinton"),
        (QUESTION_PAGE_1_5_Q2_OPTION_C, "Other"),
        (QUESTION_PAGE_1_5_Q2_OPTION_D, "Don't know"),
        (QUESTION_PAGE_1_5_Q2_OPTION_E, "Refuse to answer"),
    )

    # Are your political views closer to...
    QUESTION_PAGE_1_5_Q3_OPTION_A = "democrats"
    QUESTION_PAGE_1_5_Q3_OPTION_B = "republicans"
    QUESTION_PAGE_1_5_Q3_OPTION_C = "other"
    QUESTION_PAGE_1_5_Q3_OPTION_D = "no_preference"
    QUESTION_PAGE_1_5_Q3_OPTION_E = "dont_know"
    QUESTION_PAGE_1_5_Q3_OPTION_F = "refuse_to_answer"
    QUESTION_PAGE_1_5_Q3_CHOICES = (
        (QUESTION_PAGE_1_5_Q3_OPTION_A, "The Democrats"),
        (QUESTION_PAGE_1_5_Q3_OPTION_B, "The Republicans"),
        (QUESTION_PAGE_1_5_Q3_OPTION_C, "Other"),
        (QUESTION_PAGE_1_5_Q3_OPTION_D, "No preference"),
        (QUESTION_PAGE_1_5_Q3_OPTION_E, "Don't know"),
        (QUESTION_PAGE_1_5_Q3_OPTION_F, "Refuse to answer"),
    )

    # Valid question2 choices:
    # ------------------------
    # TODO: This question is more complex than the others and is still in need
    # of validation.

    # Valid question3 choices:
    # ------------------------
    # Which do you think is your main source of news?
    QUESTION_PAGE_3_Q1_OPTION_A = "abc_nbc_cbs"
    QUESTION_PAGE_3_Q1_OPTION_B = "cnn"
    QUESTION_PAGE_3_Q1_OPTION_C = "fox_news"
    QUESTION_PAGE_3_Q1_OPTION_D = "local_tv_radio"
    QUESTION_PAGE_3_Q1_OPTION_E = "msnbc"
    QUESTION_PAGE_3_Q1_OPTION_F = "npr_pbs"
    QUESTION_PAGE_3_Q1_OPTION_G = "newspapers"
    QUESTION_PAGE_3_Q1_OPTION_H = "facebook"
    QUESTION_PAGE_3_Q1_OPTION_I = "twitter"
    QUESTION_PAGE_3_Q1_CHOICES = (
        (QUESTION_PAGE_3_Q1_OPTION_A, "ABC, NBC, or CBS"),
        (QUESTION_PAGE_3_Q1_OPTION_B, "CNN"),
        (QUESTION_PAGE_3_Q1_OPTION_C, "Fox News"),
        (QUESTION_PAGE_3_Q1_OPTION_D, "Local TV or radio"),
        (QUESTION_PAGE_3_Q1_OPTION_E, "MSNBC"),
        (QUESTION_PAGE_3_Q1_OPTION_F, "NPR (National Public Radio) or PBS"),
        (QUESTION_PAGE_3_Q1_OPTION_G, "Newspapers, online or in paper"),
        (QUESTION_PAGE_3_Q1_OPTION_H, "Facebook"),
        (QUESTION_PAGE_3_Q1_OPTION_I, "Twitter"),
    )

    # Are there Muslims living in your neighborhood?
    QUESTION_PAGE_3_Q2_OPTION_A = "many"
    QUESTION_PAGE_3_Q2_OPTION_B = "some"
    QUESTION_PAGE_3_Q2_OPTION_C = "none"
    QUESTION_PAGE_3_Q2_OPTION_D = "dont_know"
    QUESTION_PAGE_3_Q2_OPTION_E = "refuse_to_answer"
    QUESTION_PAGE_3_Q2_CHOICES = (
        (QUESTION_PAGE_3_Q2_OPTION_A, "Many"),
        (QUESTION_PAGE_3_Q2_OPTION_B, "Some"),
        (QUESTION_PAGE_3_Q2_OPTION_C, "None at all"),
        (QUESTION_PAGE_3_Q2_OPTION_D, "Don't know"),
        (QUESTION_PAGE_3_Q2_OPTION_E, "Refuse to answer"),
    )

    # Do you have Muslim co-workers
    QUESTION_PAGE_3_Q3_OPTION_A = "many"
    QUESTION_PAGE_3_Q3_OPTION_B = "some"
    QUESTION_PAGE_3_Q3_OPTION_C = "none"
    QUESTION_PAGE_3_Q3_OPTION_D = "dont_know"
    QUESTION_PAGE_3_Q3_OPTION_E = "refuse_to_answer"
    QUESTION_PAGE_3_Q3_CHOICES = (
        (QUESTION_PAGE_3_Q3_OPTION_A, "Many"),
        (QUESTION_PAGE_3_Q3_OPTION_B, "Some"),
        (QUESTION_PAGE_3_Q3_OPTION_C, "None at all"),
        (QUESTION_PAGE_3_Q3_OPTION_D, "Don't know"),
        (QUESTION_PAGE_3_Q3_OPTION_E, "Refuse to answer"),
    )

    # Have you, personally, ever been treated unfairly due to your race,
    # ethnicity, or religion?
    QUESTION_PAGE_3_Q4_OPTION_A = "yes"
    QUESTION_PAGE_3_Q4_OPTION_B = "no"
    QUESTION_PAGE_3_Q4_OPTION_C = "dont_know"
    QUESTION_PAGE_3_Q4_OPTION_D = "refuse_to_answer"
    QUESTION_PAGE_3_Q4_CHOICES = (
        (QUESTION_PAGE_3_Q4_OPTION_A, "Yes"),
        (QUESTION_PAGE_3_Q4_OPTION_B, "No"),
        (QUESTION_PAGE_3_Q4_OPTION_C, "Don't know"),
        (QUESTION_PAGE_3_Q4_OPTION_D, "Refuse to answer"),
    )

    # Do you think people of your race or ethnicity are treated unfairly?
    QUESTION_PAGE_3_Q5_OPTION_A = "often"
    QUESTION_PAGE_3_Q5_OPTION_B = "sometimes"
    QUESTION_PAGE_3_Q5_OPTION_C = "seldom"
    QUESTION_PAGE_3_Q5_OPTION_D = "never"
    QUESTION_PAGE_3_Q5_OPTION_E = "dont_know"
    QUESTION_PAGE_3_Q5_OPTION_F = "refuse_to_answer"
    QUESTION_PAGE_3_Q5_CHOICES = (
        (QUESTION_PAGE_3_Q5_OPTION_A, "Often"),
        (QUESTION_PAGE_3_Q5_OPTION_B, "Sometimes"),
        (QUESTION_PAGE_3_Q5_OPTION_C, "Seldom"),
        (QUESTION_PAGE_3_Q5_OPTION_D, "Never"),
        (QUESTION_PAGE_3_Q5_OPTION_E, "Don't know"),
        (QUESTION_PAGE_3_Q5_OPTION_F, "Refuse to answer"),
    )

    # Do you think people of your religion are treated unfairly?
    QUESTION_PAGE_3_Q6_OPTION_A = "often"
    QUESTION_PAGE_3_Q6_OPTION_B = "sometimes"
    QUESTION_PAGE_3_Q6_OPTION_C = "seldom"
    QUESTION_PAGE_3_Q6_OPTION_D = "never"
    QUESTION_PAGE_3_Q6_OPTION_E = "dont_know"
    QUESTION_PAGE_3_Q6_OPTION_F = "refuse_to_answer"
    QUESTION_PAGE_3_Q6_CHOICES = (
        (QUESTION_PAGE_3_Q6_OPTION_A, "Often"),
        (QUESTION_PAGE_3_Q6_OPTION_B, "Sometimes"),
        (QUESTION_PAGE_3_Q6_OPTION_C, "Seldom"),
        (QUESTION_PAGE_3_Q6_OPTION_D, "Never"),
        (QUESTION_PAGE_3_Q6_OPTION_E, "Don't know"),
        (QUESTION_PAGE_3_Q6_OPTION_F, "Refuse to answer"),
    )

    # Generally speaking, would you say that most people can be trusted or that
    # you can’t be too careful in dealing with people?
    QUESTION_PAGE_3_Q7_OPTION_A = "most_people"
    QUESTION_PAGE_3_Q7_OPTION_B = "cant_be_too_careful"
    QUESTION_PAGE_3_Q7_OPTION_C = "dont_know"
    QUESTION_PAGE_3_Q7_OPTION_D = "refuse_to_answer"
    QUESTION_PAGE_3_Q7_CHOICES = (
        (QUESTION_PAGE_3_Q7_OPTION_A, "Most people can be trusted"),
        (QUESTION_PAGE_3_Q7_OPTION_B, "Can't be too careful"),
        (QUESTION_PAGE_3_Q7_OPTION_C, "Don't know"),
        (QUESTION_PAGE_3_Q7_OPTION_D, "Refuse to answer"),
    )

    # What about the next 12 months? Do you expect the national economy to get
    # better, get worse, or stay about the same?
    QUESTION_PAGE_3_Q8_OPTION_A = "get_better"
    QUESTION_PAGE_3_Q8_OPTION_B = "stay_the_same"
    QUESTION_PAGE_3_Q8_OPTION_C = "get_worse"
    QUESTION_PAGE_3_Q8_OPTION_D = "dont_know"
    QUESTION_PAGE_3_Q8_OPTION_E = "refuse_to_answer"
    QUESTION_PAGE_3_Q8_CHOICES = (
        (QUESTION_PAGE_3_Q8_OPTION_A, "Get better"),
        (QUESTION_PAGE_3_Q8_OPTION_B, "Stay the same"),
        (QUESTION_PAGE_3_Q8_OPTION_C, "Get worse"),
        (QUESTION_PAGE_3_Q8_OPTION_D, "Don't know"),
        (QUESTION_PAGE_3_Q8_OPTION_E, "Refuse to answer"),
    )

    # How concerned are you about the rise of Islamic extremism in the U.S.?
    QUESTION_PAGE_3_Q9_OPTION_A = "very_concerned"
    QUESTION_PAGE_3_Q9_OPTION_B = "somewhat_concerned"
    QUESTION_PAGE_3_Q9_OPTION_C = "not_too_concerned"
    QUESTION_PAGE_3_Q9_OPTION_D = "not_concerned"
    QUESTION_PAGE_3_Q9_OPTION_E = "dont_know"
    QUESTION_PAGE_3_Q9_OPTION_F = "refuse_to_answer"
    QUESTION_PAGE_3_Q9_CHOICES = (
        (QUESTION_PAGE_3_Q9_OPTION_A, "Very concerned"),
        (QUESTION_PAGE_3_Q9_OPTION_B, "Somewhat concerned"),
        (QUESTION_PAGE_3_Q9_OPTION_C, "Not too concerned"),
        (QUESTION_PAGE_3_Q9_OPTION_D, "Not concerned"),
        (QUESTION_PAGE_3_Q9_OPTION_E, "Don't know"),
        (QUESTION_PAGE_3_Q9_OPTION_F, "Refuse to answer"),
    )

    # In general, how well do you think the American government is doing in
    # reducing the threat of terrorism?
    QUESTION_PAGE_3_Q10_OPTION_A = "very_well"
    QUESTION_PAGE_3_Q10_OPTION_B = "fairly_well"
    QUESTION_PAGE_3_Q10_OPTION_C = "not_very_well"
    QUESTION_PAGE_3_Q10_OPTION_D = "not_well_at_all"
    QUESTION_PAGE_3_Q10_OPTION_E = "dont_know"
    QUESTION_PAGE_3_Q10_OPTION_F = "refuse_to_answer"
    QUESTION_PAGE_3_Q10_CHOICES = (
        (QUESTION_PAGE_3_Q10_OPTION_A, "Very well"),
        (QUESTION_PAGE_3_Q10_OPTION_B, "Fairly well"),
        (QUESTION_PAGE_3_Q10_OPTION_C, "Not very well"),
        (QUESTION_PAGE_3_Q10_OPTION_D, "Not well at all"),
        (QUESTION_PAGE_3_Q10_OPTION_E, "Don't know"),
        (QUESTION_PAGE_3_Q10_OPTION_F, "Refuse to answer"),
    )
    ###########################################################################

    user = models.OneToOneField(
        InvestmentGameUser, on_delete=models.CASCADE, primary_key=True
    )
    respondent = models.CharField(max_length=256, choices=RESPONDENT_CHOICES, null=True)

    # User progress tracking
    started_experiment = models.DateTimeField(
        null=True, help_text="When the user landed on the welcome page"
    )
    reached_stage = models.CharField(
        max_length=256, choices=STAGE_CHOICES, default=STAGE_SELECT_RESPONDENT,
    )
    started_select_respondent = models.DateTimeField(
        null=True, help_text="When the user landed on the select respondent stage"
    )
    started_user_investment = models.DateTimeField(
        null=True, help_text="When the user landed on the user investment stage"
    )
    started_respondent_investment = models.DateTimeField(
        null=True, help_text="When the user landed on the respondent investment stage"
    )
    started_compare = models.DateTimeField(
        null=True, help_text="When the user landed on the compare stage"
    )
    started_question_1 = models.DateTimeField(
        null=True, help_text="When the user landed on the question 1 stage"
    )
    started_question_1_5 = models.DateTimeField(
        null=True,
        help_text="When the user landed on the question 1.5 stage (if relevant)",
    )
    started_question_2 = models.DateTimeField(
        null=True, help_text="When the user landed on the question 2 stage"
    )
    started_question_3 = models.DateTimeField(
        null=True, help_text="When the user landed on the question 3 stage"
    )
    started_finish = models.DateTimeField(
        null=True,
        help_text="When the user landed on the finish stage, and completed the experiment",
    )

    # Investment game data
    user_investment = models.IntegerField(null=True)
    respondent_investment_guess = models.IntegerField(null=True)
    respondent_investment = models.IntegerField(null=True)
    user_bonus = models.IntegerField(choices=USER_BONUS_CHOICES, null=True)
    user_received = models.IntegerField(null=True)

    # Final qustionnaires
    us_citizen = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_1_Q1_CHOICES,
        help_text="Are you a U.S. citizen?",
    )
    voted_last_election = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_1_5_Q1_CHOICES,
        help_text="Did you vote for a presidential candidate in the last election?",
    )
    how_voted = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_1_5_Q2_CHOICES,
        help_text="Whom did you vote for?",
    )
    political_views = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_1_5_Q3_CHOICES,
        help_text="Are your political views generally closer to...",
    )
    multiple_agreement_question = models.CharField(max_length=255, null=True)
    multiple_agreement_question_type = models.CharField(
        max_length=255, choices=MULTIPLE_AGREEMENT_CHOICES, null=True
    )
    news_source = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_3_Q1_CHOICES,
        help_text="Which do you think is your main source of news?",
    )
    muslims_in_neighborhood = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_3_Q2_CHOICES,
        help_text="Are there Muslims living in your neighborhood?",
    )
    muslim_coworkers = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_3_Q3_CHOICES,
        help_text="Do you have Muslim co-workers?",
    )
    self_treated_unfairly = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_3_Q4_CHOICES,
        help_text="Have you, personally, ever been treated unfairly due to your race, ethnicity, or religion?",
    )
    race_treated_unfairly = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_3_Q5_CHOICES,
        help_text="Do you think people of your race or ethnicity are treated unfairly?",
    )
    religion_treated_unfairly = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_3_Q6_CHOICES,
        help_text="Do you think people of your religion are treated unfairly?",
    )
    general_trustworthiness = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_3_Q7_CHOICES,
        help_text="Generally speaking, would you say that most people can be trusted or that you can’t be too careful in dealing with people?",
    )
    economic_outlook = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_3_Q8_CHOICES,
        help_text="What about the next 12 months? Do you expect the national economy to get better, get worse, or stay about the same?",
    )
    islamic_extremism = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_3_Q9_CHOICES,
        help_text="How concerned are you about the rise of Islamic extremism in the U.S.?",
    )
    reducing_terrorism = models.CharField(
        max_length=255,
        null=True,
        choices=QUESTION_PAGE_3_Q10_CHOICES,
        help_text="In general, how well do you think the American government is doing in reducing the threat of terrorism?",
    )

    def __str__(self):
        return self.user.username
