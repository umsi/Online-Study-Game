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
    require_unique_id_query_param,
    disallow_id_session_param,
)


GUESS_THRESHOLD = 1
USER_BONUS_AMOUNT = 2
USER_INVESTMENT_MULTIPLIER = 3
INITIAL_USER_COINS_NUM = 5


@require_id_query_param
@disallow_id_session_param
@require_unique_id_query_param
@require_GET
def welcome(request, id=None):
    if request.session.get("id", None) is not None:
        try:
            # If we're loading the welcome page and an `id` session param
            # already exists, it's probably because the user did not finish a
            # previous session or has attempted to use the back button. In
            # these cases we want to forward the user to the correct stage.
            user = InvestmentGameUser.objects.get(username=request.session["id"])
            investment = Investment.objects.get(user=user)

            return redirect(reverse("invest_game:%s" % investment.reached_stage))
        except (InvestmentGameUser.DoesNotExist, Investment.DoesNotExist) as e:
            pass

    request.session["id"] = id
    request.session["started_experiment"] = json.dumps(
        timezone.now(), cls=DjangoJSONEncoder
    )

    return render(request, "welcome.html")


@require_id_session_param
@require_POST
def sign_in(request, id=None):
    """
    
    POST
    ----

    Create a new InvestmentGameUser and Investment.
    """
    user, _ = InvestmentGameUser.objects.get_or_create(username=id)
    Investment.objects.get_or_create(
        user=user,
        started_experiment=json.loads(request.session.get("started_experiment", "")),
        started_select_respondent=timezone.now(),
    )

    return redirect(reverse("invest_game:select_respondent"))


@require_id_session_param
@require_http_methods(["GET", "POST"])
@require_stage(Investment.STAGE_SELECT_RESPONDENT)
def select_respondent(request, id=None):
    """
    
    GET
    ---

    Return the page for the respondent selection stage.


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

    Return the template for the respondent selection phase.


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



    POST
    ----

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
    if request.method == "GET":
        return render(request, "question1.html")

    if request.method == "POST":
        user = InvestmentGameUser.objects.get(username=id)
        investment = Investment.objects.get(user=user)

        us_citizen = request.POST.get("us_citizen")
        investment.us_citizen = us_citizen

        investment.reached_stage = (
            Investment.STAGE_QUESTION_1_5
            if us_citizen == "yes"
            else Investment.STAGE_QUESTION_2
        )

        if us_citizen == "yes":
            investment.started_question_1_5 = timezone.now()
        else:
            investment.started_question_2 = timezone.now()

        investment.save(
            update_fields=[
                "us_citizen",
                "reached_stage",
                "started_question_1_5",
                "started_question_2",
            ]
        )

        return redirect(
            reverse(
                "invest_game:question1_5"
                if us_citizen == "yes"
                else "invest_game:question2"
            )
        )


@require_id_session_param
@require_http_methods(["GET", "POST"])
@require_stage(Investment.STAGE_QUESTION_1_5)
def question1_5(request, id=None):
    if request.method == "GET":
        return render(request, "question1-5.html")

    if request.method == "POST":
        user = InvestmentGameUser.objects.get(username=id)
        investment = Investment.objects.get(user=user)

        investment.voted_last_election = request.POST.get("voted_last_election")
        investment.how_voted = request.POST.get("how_voted")
        investment.political_views = request.POST.get("political_views")
        investment.reached_stage = Investment.STAGE_QUESTION_2
        investment.started_question_2 = timezone.now()

        investment.save(
            update_fields=[
                "voted_last_election",
                "how_voted",
                "political_views",
                "reached_stage",
                "started_question_2",
            ]
        )

        return redirect(reverse("invest_game:question2"))


@require_id_session_param
@require_http_methods(["GET", "POST"])
@require_stage(Investment.STAGE_QUESTION_2)
def question2(request, id=None):
    if request.method == "GET":
        return render(request, "question2.html")

    if request.method == "POST":
        user = InvestmentGameUser.objects.get(username=id)
        investment = Investment.objects.get(user=user)

        investment.multiple_agreement_question = request.POST.get(
            "multiple_agreement_question"
        )
        investment.multiple_agreement_question_type = request.POST.get(
            "multiple_agreement_question_type"
        )
        investment.reached_stage = Investment.STAGE_QUESTION_3
        investment.started_question_3 = timezone.now()

        investment.save(
            update_fields=[
                "multiple_agreement_question",
                "multiple_agreement_question_type",
                "reached_stage",
                "started_question_3",
            ]
        )

        return redirect(reverse("invest_game:question3"))


@require_id_session_param
@require_http_methods(["GET", "POST"])
@require_stage(Investment.STAGE_QUESTION_3)
def question3(request, id=None):
    if request.method == "GET":
        return render(request, "question3.html")

    if request.method == "POST":
        user = InvestmentGameUser.objects.get(username=id)
        investment = Investment.objects.get(user=user)

        investment.news_source = request.POST.get("news_source")
        investment.muslims_in_neighborhood = request.POST.get("muslims_in_neighborhood")
        investment.muslim_coworkers = request.POST.get("muslim_coworkers")
        investment.self_treated_unfairly = request.POST.get("self_treated_unfairly")
        investment.race_treated_unfairly = request.POST.get("race_treated_unfairly")
        investment.religion_treated_unfairly = request.POST.get(
            "religion_treated_unfairly"
        )
        investment.general_trustworthiness = request.POST.get("general_trustworthiness")
        investment.economic_outlook = request.POST.get("economic_outlook")
        investment.islamic_extremism = request.POST.get("islamic_extremism")
        investment.reducing_terrorism = request.POST.get("reducing_terrorism")
        investment.reached_stage = Investment.STAGE_FINISH
        investment.started_finish = timezone.now()

        investment.save(
            update_fields=[
                "news_source",
                "muslims_in_neighborhood",
                "muslim_coworkers",
                "self_treated_unfairly",
                "race_treated_unfairly",
                "religion_treated_unfairly",
                "general_trustworthiness",
                "economic_outlook",
                "islamic_extremism",
                "reducing_terrorism",
                "reached_stage",
                "started_finish",
            ]
        )

        return redirect(reverse("invest_game:finish"))


@require_id_session_param
@require_GET
@require_stage(Investment.STAGE_FINISH)
def finish(request, id=None):
    request.session["id"] = None
    request.session["started_experiment"] = None

    return render(request, "finish.html")
