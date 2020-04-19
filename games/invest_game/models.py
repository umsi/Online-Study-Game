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
    STAGE_QUESTION_2 = "question2"
    STAGE_QUESTION_2_5 = "question2_5"
    STAGE_QUESTION_3 = "question3"
    STAGE_QUESTION_4 = "question4"
    STAGE_COMPARE = "compare"
    STAGE_FINISH = "finish"
    STAGE_CHOICES = (
        (STAGE_SELECT_RESPONDENT, "User reached respondent selection stage"),
        (STAGE_USER_INVESTMENT, "User reached user investment stage"),
        (STAGE_RESPONDENT_INVESTMENT, "User reached respondent investment stage"),
        (STAGE_QUESTION_1, "User reached question 1 stage"),
        (STAGE_QUESTION_2, "User reached question 2 stage"),
        (STAGE_QUESTION_2_5, "User reached question 2.5 stage"),
        (STAGE_QUESTION_3, "User reached question 3 stage"),
        (STAGE_QUESTION_4, "User reached question 4 stage"),
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
    # TODO: This question is more complex than the others and is still in need
    # of validation.
    multiple_agreement_question = models.CharField(max_length=255, null=True)
    multiple_agreement_question_type = models.CharField(
        max_length=255, choices=MULTIPLE_AGREEMENT_CHOICES, null=True
    )

    # Valid question2 choices:
    # ------------------------
    # Where do you get most of your news?
    news_source = models.CharField(
        max_length=255, null=True, help_text="Where do you get most of your news?",
    )

    # Generally speaking, would you say that most people can be trusted or that
    # you can’t be too careful in dealing with people?
    TRUST_PEOPLE_OPTION_A = "most_people"
    TRUST_PEOPLE_OPTION_B = "cant_be_too_careful"
    TRUST_PEOPLE_OPTION_C = "dont_know_or_refuse"
    TRUST_PEOPLE_CHOICES = (
        (TRUST_PEOPLE_OPTION_A, "Most people can be trusted"),
        (TRUST_PEOPLE_OPTION_B, "Can't be too careful"),
        (TRUST_PEOPLE_OPTION_C, "Don't know/Refuse to answer"),
    )
    general_trustworthiness = models.CharField(
        max_length=255,
        null=True,
        choices=TRUST_PEOPLE_CHOICES,
        help_text="Generally speaking, would you say that most people can be trusted or that you can’t be too careful in dealing with people?",
    )

    # Are you a U.S. citizen?
    US_CITIZEN_OPTION_A = "yes"
    US_CITIZEN_OPTION_B = "no"
    US_CITIZEN_OPTION_C = "dont_know_or_refuse"
    US_CITIZEN_CHOICES = (
        (US_CITIZEN_OPTION_A, "Yes"),
        (US_CITIZEN_OPTION_B, "No"),
        (US_CITIZEN_OPTION_C, "Don't know/Refuse to answer"),
    )
    us_citizen = models.CharField(
        max_length=255,
        null=True,
        choices=US_CITIZEN_CHOICES,
        help_text="Are you a U.S. citizen?",
    )

    # Valid question2_5 choices:
    # --------------------------
    # Did you vote for a presidential candidate in the last election?
    VOTED_PRESIDENT_OPTION_A = "yes"
    VOTED_PRESIDENT_OPTION_B = "no"
    VOTED_PRESIDENT_OPTION_C = "dont_know_or_refuse"
    VOTED_PRESIDENT_CHOICES = (
        (VOTED_PRESIDENT_OPTION_A, "Yes"),
        (VOTED_PRESIDENT_OPTION_B, "No"),
        (VOTED_PRESIDENT_OPTION_C, "Don't know/Refuse to answer"),
    )
    voted_last_election = models.CharField(
        max_length=255,
        null=True,
        choices=VOTED_PRESIDENT_CHOICES,
        help_text="Did you vote for a presidential candidate in the last election?",
    )

    # Whom did you vote for?
    HOW_VOTED_OPTION_A = "trump"
    HOW_VOTED_OPTION_B = "clinton"
    HOW_VOTED_OPTION_C = "other"
    HOW_VOTED_OPTION_D = "dont_know_or_refuse"
    HOW_VOTED_CHOICES = (
        (HOW_VOTED_OPTION_A, "Donald Trump"),
        (HOW_VOTED_OPTION_B, "Hillary Clinton"),
        (HOW_VOTED_OPTION_C, "Other"),
        (HOW_VOTED_OPTION_D, "Don't know/Refuse to answer"),
    )
    how_voted = models.CharField(
        max_length=255,
        null=True,
        choices=HOW_VOTED_CHOICES,
        help_text="Whom did you vote for?",
    )

    # Are your political views closer to those of
    POLITICAL_VIEWS_OPTION_A = "democrats"
    POLITICAL_VIEWS_OPTION_B = "republicans"
    POLITICAL_VIEWS_OPTION_C = "no_preference"
    POLITICAL_VIEWS_OPTION_D = "dont_know_or_refuse"
    POLITICAL_VIEWS_CHOICES = (
        (POLITICAL_VIEWS_OPTION_A, "The Democratic Party"),
        (POLITICAL_VIEWS_OPTION_B, "The Republican Party"),
        (POLITICAL_VIEWS_OPTION_C, "No preference"),
        (POLITICAL_VIEWS_OPTION_D, "Don't know/Refuse to answer"),
    )
    political_views = models.CharField(
        max_length=255,
        null=True,
        choices=POLITICAL_VIEWS_CHOICES,
        help_text="Are your political views generally closer to those of",
    )

    # Valid question3 choices:
    # ------------------------
    # Do you approve or disapprove of the way Donald Trump is handling his job as president?
    APPROVE_OF_TRUMP_OPTION_A = "approve"
    APPROVE_OF_TRUMP_OPTION_B = "disapprove"
    APPROVE_OF_TRUMP_OPTION_C = "dont_know_or_refuse"
    APPROVE_OF_TRUMP_CHOICES = (
        (APPROVE_OF_TRUMP_OPTION_A, "Approve"),
        (APPROVE_OF_TRUMP_OPTION_B, "Disapprove"),
        (APPROVE_OF_TRUMP_OPTION_C, "Don't know/Refuse to answer"),
    )
    approve_of_trump = models.CharField(
        max_length=255,
        null=True,
        choices=APPROVE_OF_TRUMP_CHOICES,
        help_text="Do you approve or disapprove of the way Donald Trump is handling his job as president?",
    )

    # Over the next 12 months, do you expect the national economy to get
    # better, get worse, or stay about the same?
    ECONOMIC_OUTLOOK_OPTION_A = "get_better"
    ECONOMIC_OUTLOOK_OPTION_B = "stay_the_same"
    ECONOMIC_OUTLOOK_OPTION_C = "get_worse"
    ECONOMIC_OUTLOOK_OPTION_D = "dont_know_or_refuse"
    ECONOMIC_OUTLOOK_CHOICES = (
        (ECONOMIC_OUTLOOK_OPTION_A, "Get better"),
        (ECONOMIC_OUTLOOK_OPTION_B, "Stay the same"),
        (ECONOMIC_OUTLOOK_OPTION_C, "Get worse"),
        (ECONOMIC_OUTLOOK_OPTION_D, "Don't know/Refuse to answer"),
    )
    economic_outlook = models.CharField(
        max_length=255,
        null=True,
        choices=ECONOMIC_OUTLOOK_CHOICES,
        help_text="Over the next 12 months, do you expect the national economy to get better, get worse, or stay about the same?",
    )

    # Are there Muslims living in your neighborhood?
    MUSLIMS_IN_NEIGHBORHOOD_OPTION_A = "many"
    MUSLIMS_IN_NEIGHBORHOOD_OPTION_B = "some"
    MUSLIMS_IN_NEIGHBORHOOD_OPTION_C = "none"
    MUSLIMS_IN_NEIGHBORHOOD_OPTION_D = "dont_know_or_refuse"
    MUSLIMS_IN_NEIGHBORHOOD_CHOICES = (
        (MUSLIMS_IN_NEIGHBORHOOD_OPTION_A, "Many"),
        (MUSLIMS_IN_NEIGHBORHOOD_OPTION_B, "Some"),
        (MUSLIMS_IN_NEIGHBORHOOD_OPTION_C, "None at all"),
        (MUSLIMS_IN_NEIGHBORHOOD_OPTION_D, "Don't know/Refuse to answer"),
    )
    muslims_in_neighborhood = models.CharField(
        max_length=255,
        null=True,
        choices=MUSLIMS_IN_NEIGHBORHOOD_CHOICES,
        help_text="Are there Muslims living in your neighborhood?",
    )

    # Do you have Muslim co-workers?
    MUSLIM_COWORKERS_OPTION_A = "many"
    MUSLIM_COWORKERS_OPTION_B = "some"
    MUSLIM_COWORKERS_OPTION_C = "none"
    MUSLIM_COWORKERS_OPTION_D = "dont_know_or_refuse"
    MUSLIM_COWORKERS_CHOICES = (
        (MUSLIM_COWORKERS_OPTION_A, "Many"),
        (MUSLIM_COWORKERS_OPTION_B, "Some"),
        (MUSLIM_COWORKERS_OPTION_C, "None at all"),
        (MUSLIM_COWORKERS_OPTION_D, "Don't know/Refuse to answer"),
    )
    muslim_coworkers = models.CharField(
        max_length=255,
        null=True,
        choices=MUSLIM_COWORKERS_CHOICES,
        help_text="Do you have Muslim co-workers?",
    )

    # Have you, personally, ever been treated unfairly due to your race,
    # ethnicity, or religion?
    SELF_TREATED_UNFAIRLY_OPTION_A = "yes"
    SELF_TREATED_UNFAIRLY_OPTION_B = "no"
    SELF_TREATED_UNFAIRLY_OPTION_C = "dont_know_or_refuse"
    SELF_TREATED_UNFAIRLY_CHOICES = (
        (SELF_TREATED_UNFAIRLY_OPTION_A, "Yes"),
        (SELF_TREATED_UNFAIRLY_OPTION_B, "No"),
        (SELF_TREATED_UNFAIRLY_OPTION_C, "Don't know/Refuse to answer"),
    )
    self_treated_unfairly = models.CharField(
        max_length=255,
        null=True,
        choices=SELF_TREATED_UNFAIRLY_CHOICES,
        help_text="Have you, personally, ever been treated unfairly due to your race, ethnicity, or religion?",
    )

    # Do you think people of your race or ethnicity are treated unfairly?
    RACE_TREATED_UNFAIRLY_OPTION_A = "often"
    RACE_TREATED_UNFAIRLY_OPTION_B = "sometimes"
    RACE_TREATED_UNFAIRLY_OPTION_C = "seldom"
    RACE_TREATED_UNFAIRLY_OPTION_D = "never"
    RACE_TREATED_UNFAIRLY_OPTION_E = "dont_know_or_refuse"
    RACE_TREATED_UNFAIRLY_CHOICES = (
        (RACE_TREATED_UNFAIRLY_OPTION_A, "Often"),
        (RACE_TREATED_UNFAIRLY_OPTION_B, "Sometimes"),
        (RACE_TREATED_UNFAIRLY_OPTION_C, "Seldom"),
        (RACE_TREATED_UNFAIRLY_OPTION_D, "Never"),
        (RACE_TREATED_UNFAIRLY_OPTION_E, "Don't know/Refuse to answer"),
    )
    race_treated_unfairly = models.CharField(
        max_length=255,
        null=True,
        choices=RACE_TREATED_UNFAIRLY_CHOICES,
        help_text="Do you think people of your race or ethnicity are treated unfairly?",
    )

    # Do you think people of your religion are treated unfairly?
    RELIGION_TREATED_UNFAIRLY_OPTION_A = "often"
    RELIGION_TREATED_UNFAIRLY_OPTION_B = "sometimes"
    RELIGION_TREATED_UNFAIRLY_OPTION_C = "seldom"
    RELIGION_TREATED_UNFAIRLY_OPTION_D = "never"
    RELIGION_TREATED_UNFAIRLY_OPTION_E = "dont_know_or_refuse"
    RELIGION_TREATED_UNFAIRLY_CHOICES = (
        (RELIGION_TREATED_UNFAIRLY_OPTION_A, "Often"),
        (RELIGION_TREATED_UNFAIRLY_OPTION_B, "Sometimes"),
        (RELIGION_TREATED_UNFAIRLY_OPTION_C, "Seldom"),
        (RELIGION_TREATED_UNFAIRLY_OPTION_D, "Never"),
        (RELIGION_TREATED_UNFAIRLY_OPTION_E, "Don't know/Refuse to answer"),
    )
    religion_treated_unfairly = models.CharField(
        max_length=255,
        null=True,
        choices=RELIGION_TREATED_UNFAIRLY_CHOICES,
        help_text="Do you think people of your religion are treated unfairly?",
    )

    # How concerned are you about the rise of Islamic extremism in the U.S.?
    ISLAMIC_EXTREMISM_OPTION_A = "very_concerned"
    ISLAMIC_EXTREMISM_OPTION_B = "somewhat_concerned"
    ISLAMIC_EXTREMISM_OPTION_C = "not_too_concerned"
    ISLAMIC_EXTREMISM_OPTION_D = "not_concerned"
    ISLAMIC_EXTREMISM_OPTION_E = "dont_know_or_refuse"
    ISLAMIC_EXTREMISM_CHOICES = (
        (ISLAMIC_EXTREMISM_OPTION_A, "Very concerned"),
        (ISLAMIC_EXTREMISM_OPTION_B, "Somewhat concerned"),
        (ISLAMIC_EXTREMISM_OPTION_C, "Not too concerned"),
        (ISLAMIC_EXTREMISM_OPTION_D, "Not concerned"),
        (ISLAMIC_EXTREMISM_OPTION_E, "Don't know/Refuse to answer"),
    )
    islamic_extremism = models.CharField(
        max_length=255,
        null=True,
        choices=ISLAMIC_EXTREMISM_CHOICES,
        help_text="How concerned are you about the rise of Islamic extremism in the U.S.?",
    )

    # In general, how well do you think the American government is doing in
    # reducing the threat of terrorism?
    REDUCING_TERRORISM_OPTION_A = "very_well"
    REDUCING_TERRORISM_OPTION_B = "fairly_well"
    REDUCING_TERRORISM_OPTION_C = "not_very_well"
    REDUCING_TERRORISM_OPTION_D = "not_well_at_all"
    REDUCING_TERRORISM_OPTION_E = "dont_know_or_refuse"
    REDUCING_TERRORISM_CHOICES = (
        (REDUCING_TERRORISM_OPTION_A, "Very well"),
        (REDUCING_TERRORISM_OPTION_B, "Fairly well"),
        (REDUCING_TERRORISM_OPTION_C, "Not very well"),
        (REDUCING_TERRORISM_OPTION_D, "Not well at all"),
        (REDUCING_TERRORISM_OPTION_E, "Don't know/Refuse to answer"),
    )
    reducing_terrorism = models.CharField(
        max_length=255,
        null=True,
        choices=REDUCING_TERRORISM_CHOICES,
        help_text="In general, how well do you think the American government is doing in reducing the threat of terrorism?",
    )

    # Valid question4 choices:
    # ------------------------
    # Covid-19 was a bioweapon designed by China to wage war on the United States.
    COVID_BIOWEAPON_OPTION_A = "strongly_disagree"
    COVID_BIOWEAPON_OPTION_B = "disagree"
    COVID_BIOWEAPON_OPTION_C = "neutral"
    COVID_BIOWEAPON_OPTION_D = "agree"
    COVID_BIOWEAPON_OPTION_E = "strongly_agree"
    COVID_BIOWEAPON_OPTION_F = "dont_know_or_refuse"
    COVID_BIOWEAPON_CHOICES = (
        (COVID_BIOWEAPON_OPTION_A, "Strongly disagree"),
        (COVID_BIOWEAPON_OPTION_B, "Disagree"),
        (COVID_BIOWEAPON_OPTION_C, "Neutral"),
        (COVID_BIOWEAPON_OPTION_D, "Agree"),
        (COVID_BIOWEAPON_OPTION_E, "Strongly agree"),
        (COVID_BIOWEAPON_OPTION_F, "Don't know/Refuse to answer"),
    )
    covid_bioweapon = models.CharField(
        max_length=255,
        null=True,
        choices=COVID_BIOWEAPON_CHOICES,
        help_text="Covid-19 was a bioweapon designed by China to wage war on the United States.",
    )

    # Who is more to blame for the coronavirus pandemic in the United States?
    COVID_BLAME_OPTION_A = "chinese_government"
    COVID_BLAME_OPTION_B = "united_states_government"
    COVID_BLAME_OPTION_C = "equally_responsible"
    COVID_BLAME_OPTION_D = "dont_know_or_refuse"
    COVID_BLAME_CHOICES = (
        (COVID_BLAME_OPTION_A, "The Chinese government"),
        (COVID_BLAME_OPTION_B, "The United States government"),
        (COVID_BLAME_OPTION_C, "They are equally responsible"),
        (COVID_BLAME_OPTION_D, "Don't know/Refuse to answer"),
    )
    covid_blame = models.CharField(
        max_length=255,
        null=True,
        choices=COVID_BLAME_CHOICES,
        help_text="Who is more to blame for the coronavirus pandemic in the United States?",
    )

    # Now that the U.S. has experienced shortages of medical equipment, we should share our masks, ventilators, and other lifesaving equipment with other countries after the virus subsides here.
    SHARE_EQUIPMENT_OPTION_A = "strongly_disagree"
    SHARE_EQUIPMENT_OPTION_B = "disagree"
    SHARE_EQUIPMENT_OPTION_C = "neutral"
    SHARE_EQUIPMENT_OPTION_D = "agree"
    SHARE_EQUIPMENT_OPTION_E = "strongly_agree"
    SHARE_EQUIPMENT_OPTION_F = "dont_know_or_refuse"
    SHARE_EQUIPMENT_CHOICES = (
        (SHARE_EQUIPMENT_OPTION_A, "Strongly disagree"),
        (SHARE_EQUIPMENT_OPTION_B, "Disagree"),
        (SHARE_EQUIPMENT_OPTION_C, "Neutral"),
        (SHARE_EQUIPMENT_OPTION_D, "Agree"),
        (SHARE_EQUIPMENT_OPTION_E, "Strongly agree"),
        (SHARE_EQUIPMENT_OPTION_F, "Don't know/Refuse to answer"),
    )
    share_equipment = models.CharField(
        max_length=255,
        null=True,
        choices=SHARE_EQUIPMENT_CHOICES,
        help_text="Now that the U.S. has experienced shortages of medical equipment, we should share our masks, ventilators, and other lifesaving equipment with other countries after the virus subsides here.",
    )

    # Covid-19 can only be beaten if countries cooperate in finding treatments and a vaccine.
    COOPERATE_TREATMENT_OPTION_A = "strongly_disagree"
    COOPERATE_TREATMENT_OPTION_B = "disagree"
    COOPERATE_TREATMENT_OPTION_C = "neutral"
    COOPERATE_TREATMENT_OPTION_D = "agree"
    COOPERATE_TREATMENT_OPTION_E = "strongly_agree"
    COOPERATE_TREATMENT_OPTION_F = "dont_know_or_refuse"
    COOPERATE_TREATMENT_CHOICES = (
        (COOPERATE_TREATMENT_OPTION_A, "Strongly disagree"),
        (COOPERATE_TREATMENT_OPTION_B, "Disagree"),
        (COOPERATE_TREATMENT_OPTION_C, "Neutral"),
        (COOPERATE_TREATMENT_OPTION_D, "Agree"),
        (COOPERATE_TREATMENT_OPTION_E, "Strongly agree"),
        (COOPERATE_TREATMENT_OPTION_F, "Don't know/Refuse to answer"),
    )
    cooperate_treatment = models.CharField(
        max_length=255,
        null=True,
        choices=COOPERATE_TREATMENT_CHOICES,
        help_text="Covid-19 can only be beaten if countries cooperate in finding treatments and a vaccine.",
    )

    # Ventilators for patients over 65
    OVER_65_VENTILATORS_OPTION_A = "1"
    OVER_65_VENTILATORS_OPTION_B = "2"
    OVER_65_VENTILATORS_OPTION_C = "3"
    OVER_65_VENTILATORS_OPTION_D = "4"
    OVER_65_VENTILATORS_OPTION_E = "5"
    OVER_65_VENTILATORS_OPTION_F = "dont_know_or_refuse"
    OVER_65_VENTILATORS_CHOICES = (
        (OVER_65_VENTILATORS_OPTION_A, "Never gets a ventilator"),
        (OVER_65_VENTILATORS_OPTION_B, "2"),
        (OVER_65_VENTILATORS_OPTION_C, "3"),
        (OVER_65_VENTILATORS_OPTION_D, "4"),
        (OVER_65_VENTILATORS_OPTION_E, "Always gets a ventilator"),
        (OVER_65_VENTILATORS_OPTION_F, "Don't know/Refuse to answer"),
    )
    over_65_ventilators = models.CharField(
        max_length=255,
        null=True,
        choices=OVER_65_VENTILATORS_CHOICES,
        help_text="Ventilators for patients over 65",
    )

    # Ventilators for non-U.S. citizens
    NON_US_CITIZENS_VENTILATORS_OPTION_A = "1"
    NON_US_CITIZENS_VENTILATORS_OPTION_B = "2"
    NON_US_CITIZENS_VENTILATORS_OPTION_C = "3"
    NON_US_CITIZENS_VENTILATORS_OPTION_D = "4"
    NON_US_CITIZENS_VENTILATORS_OPTION_E = "5"
    NON_US_CITIZENS_VENTILATORS_OPTION_F = "dont_know_or_refuse"
    NON_US_CITIZENS_VENTILATORS_CHOICES = (
        (NON_US_CITIZENS_VENTILATORS_OPTION_A, "Never gets a ventilator"),
        (NON_US_CITIZENS_VENTILATORS_OPTION_B, "2"),
        (NON_US_CITIZENS_VENTILATORS_OPTION_C, "3"),
        (NON_US_CITIZENS_VENTILATORS_OPTION_D, "4"),
        (NON_US_CITIZENS_VENTILATORS_OPTION_E, "Always gets a ventilator"),
        (NON_US_CITIZENS_VENTILATORS_OPTION_F, "Don't know/Refuse to answer"),
    )
    non_us_citizens_ventilators = models.CharField(
        max_length=255,
        null=True,
        choices=NON_US_CITIZENS_VENTILATORS_CHOICES,
        help_text="Ventilators for non-U.S. citizens",
    )

    # Ventilators for Muslim-Americans
    MUSLIM_AMERICANS_VENTILATORS_OPTION_A = "1"
    MUSLIM_AMERICANS_VENTILATORS_OPTION_B = "2"
    MUSLIM_AMERICANS_VENTILATORS_OPTION_C = "3"
    MUSLIM_AMERICANS_VENTILATORS_OPTION_D = "4"
    MUSLIM_AMERICANS_VENTILATORS_OPTION_E = "5"
    MUSLIM_AMERICANS_VENTILATORS_OPTION_F = "dont_know_or_refuse"
    MUSLIM_AMERICANS_VENTILATORS_CHOICES = (
        (MUSLIM_AMERICANS_VENTILATORS_OPTION_A, "Never gets a ventilator"),
        (MUSLIM_AMERICANS_VENTILATORS_OPTION_B, "2"),
        (MUSLIM_AMERICANS_VENTILATORS_OPTION_C, "3"),
        (MUSLIM_AMERICANS_VENTILATORS_OPTION_D, "4"),
        (MUSLIM_AMERICANS_VENTILATORS_OPTION_E, "Always gets a ventilator"),
        (MUSLIM_AMERICANS_VENTILATORS_OPTION_F, "Don't know/Refuse to answer"),
    )
    muslim_americans_ventilators = models.CharField(
        max_length=255,
        null=True,
        choices=MUSLIM_AMERICANS_VENTILATORS_CHOICES,
        help_text="Ventilators for Muslim Americans",
    )

    # Ventilators for Chinese-Americans
    CHINESE_AMERICANS_VENTILATORS_OPTION_A = "1"
    CHINESE_AMERICANS_VENTILATORS_OPTION_B = "2"
    CHINESE_AMERICANS_VENTILATORS_OPTION_C = "3"
    CHINESE_AMERICANS_VENTILATORS_OPTION_D = "4"
    CHINESE_AMERICANS_VENTILATORS_OPTION_E = "5"
    CHINESE_AMERICANS_VENTILATORS_OPTION_F = "dont_know_or_refuse"
    CHINESE_AMERICANS_VENTILATORS_CHOICES = (
        (CHINESE_AMERICANS_VENTILATORS_OPTION_A, "Never gets a ventilator"),
        (CHINESE_AMERICANS_VENTILATORS_OPTION_B, "2"),
        (CHINESE_AMERICANS_VENTILATORS_OPTION_C, "3"),
        (CHINESE_AMERICANS_VENTILATORS_OPTION_D, "4"),
        (CHINESE_AMERICANS_VENTILATORS_OPTION_E, "Always gets a ventilator"),
        (CHINESE_AMERICANS_VENTILATORS_OPTION_F, "Don't know/Refuse to answer"),
    )
    chinese_americans_ventilators = models.CharField(
        max_length=255,
        null=True,
        choices=CHINESE_AMERICANS_VENTILATORS_CHOICES,
        help_text="Ventilators for Chinese Americans",
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
    reached_stage = models.CharField(max_length=256, choices=STAGE_CHOICES, null=True,)
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
    started_question_2 = models.DateTimeField(
        null=True, help_text="When the user landed on the question 2 stage"
    )
    started_question_2_5 = models.DateTimeField(
        null=True,
        help_text="When the user landed on the question 2.5 stage (if relevant)",
    )
    started_question_3 = models.DateTimeField(
        null=True, help_text="When the user landed on the question 3 stage"
    )
    started_question_4 = models.DateTimeField(
        null=True, help_text="When the user landed on the question 4 stage"
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

    def __str__(self):
        return self.user.username
