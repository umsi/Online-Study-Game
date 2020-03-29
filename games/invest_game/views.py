import os
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.six.moves import range
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.urls import reverse

from config.settings import DATA_ADDR, INFO_STORE
from .models import Investment, InvestmentGameUser
from games.core.decorators import (
    require_id_session_param,
    require_id_query_param,
)
from .decorators import (
    require_stage,
    require_unique_id_query_param_and_disallow_id_session_param,
)


GUESS_THRESHOLD = 1
USER_BONUS_AMOUNT = 2
USER_INVESTMENT_MULTIPLIER = 3
INITIAL_USER_COINS_NUM = 5


@require_unique_id_query_param_and_disallow_id_session_param
@require_http_methods(["GET", "POST"])
def welcome(request, id=None):
    if request.method == "GET":
        request.session["id"] = id
        # TODO: I'm not sure it's ideal to be altering the database on a GET
        # request as we do here, though this view is guarded somewhat by the
        # decorators above. But maybe there's a better way to handle this?
        user = InvestmentGameUser.objects.create(username=id)
        Investment.objects.create(
            user=user, started_experiment=timezone.now(),
        )

        return render(request, "welcome.html")

    if request.method == "POST":
        user = InvestmentGameUser.objects.get(username=id)
        investment = Investment.objects.get(user=user)
        investment.started_select_respondent = timezone.now()
        investment.reached_stage = Investment.STAGE_SELECT_RESPONDENT

        investment.save(
            update_fields=["started_user_investment", "reached_stage"]
        )

        return HttpResponse()


@require_id_session_param
@require_http_methods(["GET", "POST"])
@require_stage(Investment.STAGE_SELECT_RESPONDENT)
def select_respondent(request, id=None):
    """
    GET
    ---

    Render the page for the respondent selection stage.


    POST
    ----

    Record the user's selected respondent.
    """
    if request.method == "GET":
        return render(request, "select_respondent.html")

    if request.method == "POST":
        user = InvestmentGameUser.objects.get(username=id)
        investment = Investment.objects.get(user=user)
        investment.reached_stage = Investment.STAGE_USER_INVESTMENT
        investment.started_user_investment = timezone.now()
        investment.save(
            update_fields=["reached_stage", "started_user_investment",]
        )

        respondent = request.POST.get("respondent", None)

        if investment.respondent is None:
            investment.respondent = respondent
            investment.save(update_fields=["respondent"])
            investment.refresh_from_db()  # TODO: is this needed?

        return HttpResponse(investment.respondent)


@require_id_session_param
@require_http_methods(["GET", "POST"])
@require_stage(Investment.STAGE_USER_INVESTMENT)
def user_investment(request, id=None):
    """
    GET
    ---

    Render the template for the user investment phase.


    POST
    ----

    Record the user's selected respondent.
    """
    user = InvestmentGameUser.objects.get(username=id)
    investment = Investment.objects.get(user=user)

    if request.method == "GET":
        context = {
            "respondent": investment.respondent,
            "investor_coins": range(20),
            "respondent_coins": range(20),
        }

        return render(request, "user_investment.html", context)

    if request.method == "POST":
        investment.started_respondent_investment = timezone.now()
        investment.user_investment = int(request.POST.get("user_investment"))
        investment.reached_stage = Investment.STAGE_RESPONDENT_INVESTMENT
        investment.save(
            update_fields=[
                "started_respondent_investment",
                "user_investment",
                "reached_stage",
            ]
        )

        return redirect(reverse("invest_game:respondent_investment"))


@require_id_session_param
@require_http_methods(["GET", "POST"])
@require_stage(Investment.STAGE_RESPONDENT_INVESTMENT)
def respondent_investment(request, id=None):
    """
    
    GET
    ---

    Render the template for the respondent investment phase.


    POST
    ----

    Record the user's respondent investment guess.
    """
    user = InvestmentGameUser.objects.get(username=id)
    investment = Investment.objects.get(user=user)

    if request.method == "GET":
        return render(
            request,
            "respondent_investment.html",
            {
                "respondent": investment.respondent,
                "user_investment": investment.user_investment,
                "USER_INVESTMENT_MULTIPLIER": USER_INVESTMENT_MULTIPLIER,
                "investor_coins": range(20),
                "respondent_coins": range(20),
            },
        )

    if request.method == "POST":
        data = {}
        data_path = os.path.join(DATA_ADDR, "ans.json")
        with open(data_path) as json_file:
            data = json.load(json_file)

        # The *actual* amount returned by the respondent, obtained from a
        # hard-coded data file:
        respondent_investment = data.get(investment.respondent, {}).get(
            str(investment.user_investment)
        )
        respondent_investment_guess = int(
            request.POST.get("respondent_investment_guess")
        )

        # NOTE: The final amount the user received is calculated as follows:
        #  - The *actual* amount the respondent invested
        #  - Plus a bonus of $2 if the user guess was within the
        #    `GUESS_THRESHOLD`
        #  - Plus the difference between `INITIAL_USER_COINS_NUM` and the
        #    amount the user decided to invest in the respondent.
        user_received = respondent_investment
        user_bonus = 0
        if abs(respondent_investment - respondent_investment_guess) <= GUESS_THRESHOLD:
            user_bonus = USER_BONUS_AMOUNT
            user_received += user_bonus
        user_received += INITIAL_USER_COINS_NUM - investment.user_investment

        investment.respondent_investment = respondent_investment
        investment.started_compare = timezone.now()
        investment.respondent_investment_guess = respondent_investment_guess
        investment.user_received = user_received
        investment.user_bonus = user_bonus
        investment.reached_stage = Investment.STAGE_COMPARE
        investment.save(
            update_fields=[
                "respondent_investment",
                "started_compare",
                "respondent_investment_guess",
                "user_received",
                "user_bonus",
                "reached_stage",
            ]
        )

        return redirect(reverse("invest_game:compare"))


@require_id_session_param
@require_http_methods(["GET", "POST"])
@require_stage(Investment.STAGE_COMPARE)
def compare(request, id=None):
    """
    
    GET
    ---

    Calculate comparison statistics and render the template for the compare 
    phase.


    POST
    ----

    Redirect to next stage.
    """
    user = InvestmentGameUser.objects.get(username=id)
    investment = Investment.objects.get(user=user)

    if request.method == "GET":
        guess_flag = "not within"
        if (
            abs(
                investment.respondent_investment
                - investment.respondent_investment_guess
            )
            <= GUESS_THRESHOLD
        ):
            guess_flag = "within"

        context = {
            "user_investment": investment.user_investment,
            "respondent_investment_guess": investment.respondent_investment_guess,
            "respondent_investment": investment.respondent_investment,
            "received": investment.user_received,
            "respondent": investment.respondent,
            "guess_flag": guess_flag,
            "user_left": INITIAL_USER_COINS_NUM - investment.user_investment,
            "user_bonus": investment.user_bonus,
        }

        return render(request, "compare.html", context)

    if request.method == "POST":
        investment.reached_stage = Investment.STAGE_QUESTION_1
        investment.started_question_1 = timezone.now()
        investment.save(update_fields=["reached_stage", "started_question_1"])

        return redirect(reverse("invest_game:question1"))


# TODO: Use Django's ModelForms to handle this view and subsequent
# questionnaire views.
@require_id_session_param
@require_http_methods(["GET", "POST"])
@require_stage(Investment.STAGE_QUESTION_1)
def question1(request, id=None):
    """
    
    GET
    ---

    Render the template for the question1 (multiple agreement) phase.


    POST
    ----

    Record questionnaire responses and redirect to next stage.
    """
    if request.method == "GET":
        return render(request, "question1.html")

    if request.method == "POST":
        user = InvestmentGameUser.objects.get(username=id)
        investment = Investment.objects.get(user=user)

        data = json.loads(request.body)
        investment.multiple_agreement_question = data["multiple_agreement_question"]
        investment.multiple_agreement_question_type = data[
            "multiple_agreement_question_type"
        ]
        investment.reached_stage = Investment.STAGE_QUESTION_2
        investment.started_question_2 = timezone.now()

        investment.save(
            update_fields=[
                "multiple_agreement_question",
                "multiple_agreement_question_type",
                "reached_stage",
                "started_question_2",
            ]
        )

        return HttpResponse()


@require_id_session_param
@require_http_methods(["GET", "POST"])
@require_stage(Investment.STAGE_QUESTION_2)
def question2(request, id=None):
    """
    
    GET
    ---

    Render the template for the question2 (news and U.S. citizenship) phase.


    POST
    ----

    Record questionnaire responses and redirect to next stage.
    """
    if request.method == "GET":
        return render(request, "question2.html")

    if request.method == "POST":
        user = InvestmentGameUser.objects.get(username=id)
        investment = Investment.objects.get(user=user)

        data = json.loads(request.body)
        investment.general_trustworthiness = data["general_trustworthiness"]
        investment.news_source = str(data["news_source"])
        investment.political_views = data["political_views"]
        investment.us_citizen = data["us_citizen"]

        investment.reached_stage = (
            Investment.STAGE_QUESTION_2_5
            if data["us_citizen"] == "yes"
            else Investment.STAGE_QUESTION_3
        )

        if data["us_citizen"] == "yes":
            investment.started_question_2_5 = timezone.now()
        else:
            investment.started_question_3 = timezone.now()

        investment.save(
            update_fields=[
                "general_trustworthiness",
                "news_source",
                "political_views",
                "us_citizen",
                "reached_stage",
                "started_question_2_5",
                "started_question_3",
            ]
        )

        return HttpResponse(
            json.dumps(
                {
                    "redirect_location": "question2_5"
                    if data["us_citizen"] == "yes"
                    else "question3"
                }
            ),
            content_type="application/json",
        )


@require_id_session_param
@require_http_methods(["GET", "POST"])
@require_stage(Investment.STAGE_QUESTION_2_5)
def question2_5(request, id=None):
    """
    
    GET
    ---

    Render the template for the question2-5 (voting questions) phase.


    POST
    ----

    Record questionnaire responses and redirect to next stage.
    """
    if request.method == "GET":
        return render(request, "question2-5.html")

    if request.method == "POST":
        user = InvestmentGameUser.objects.get(username=id)
        investment = Investment.objects.get(user=user)
        data = json.loads(request.body)

        investment.voted_last_election = data["voted_last_election"]
        investment.how_voted = data["how_voted"]
        investment.reached_stage = Investment.STAGE_QUESTION_3
        investment.started_question_3 = timezone.now()

        investment.save(
            update_fields=[
                "voted_last_election",
                "how_voted",
                "reached_stage",
                "started_question_3",
            ]
        )

        return HttpResponse()


@require_id_session_param
@require_http_methods(["GET", "POST"])
@require_stage(Investment.STAGE_QUESTION_3)
def question3(request, id=None):
    """
    
    GET
    ---

    Render the template for the question2 (news consumption habits) phase.


    POST
    ----

    Record questionnaire responses and redirect to next stage.
    """
    if request.method == "GET":
        return render(request, "question3.html")

    if request.method == "POST":
        user = InvestmentGameUser.objects.get(username=id)
        investment = Investment.objects.get(user=user)
        data = json.loads(request.body)

        investment.approve_of_trump = data["approve_of_trump"]
        investment.muslims_in_neighborhood = data["muslims_in_neighborhood"]
        investment.muslim_coworkers = data["muslim_coworkers"]
        investment.self_treated_unfairly = data["self_treated_unfairly"]
        investment.race_treated_unfairly = data["race_treated_unfairly"]
        investment.religion_treated_unfairly = data["religion_treated_unfairly"]
        investment.economic_outlook = data["economic_outlook"]
        investment.islamic_extremism = data["islamic_extremism"]
        investment.reducing_terrorism = data["reducing_terrorism"]
        investment.reached_stage = Investment.STAGE_FINISH
        investment.started_finish = timezone.now()

        investment.save(
            update_fields=[
                "approve_of_trump",
                "muslims_in_neighborhood",
                "muslim_coworkers",
                "self_treated_unfairly",
                "race_treated_unfairly",
                "religion_treated_unfairly",
                "economic_outlook",
                "islamic_extremism",
                "reducing_terrorism",
                "reached_stage",
                "started_finish",
            ]
        )

        return HttpResponse()


@require_id_session_param
@require_GET
@require_stage(Investment.STAGE_FINISH)
def finish(request, id=None):
    """
    
    GET
    ---

    Render the template for the finish phase and reset the id session param.
    """
    request.session["id"] = None
    request.session["started_experiment"] = None

    return render(request, "finish.html")
