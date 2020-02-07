import os
import json
import datetime
import random

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.six.moves import range
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.urls import reverse

from config.settings import DATA_ADDR, INFO_STORE
from .models import Investment, InvestmentGameUser
from games.core.decorators import (
    require_id_session_param,
    require_id_query_param,
)
from .decorators import require_stage


GUESS_THRESHOLD = 1
USER_BONUS_AMOUNT = 2


@require_id_query_param
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
    Investment.objects.get_or_create(user=user)

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
        investment.save(update_fields=["reached_stage"])

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
        investment.started_user_investment = datetime.datetime.now()
        investment.save(update_fields=["started_user_investment"])

        return render(
            request, "user_investment.html", {"respondent": investment.respondent}
        )

    if request.method == "POST":
        investment.finished_user_investment = datetime.datetime.now()
        investment.user_investment = int(request.POST.get("user_investment"))
        investment.reached_stage = Investment.STAGE_RESPONDENT_INVESTMENT
        investment.save(
            update_fields=[
                "finished_user_investment",
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
        investment.started_respondent_investment = datetime.datetime.now()
        investment.save(update_fields=["started_respondent_investment"])

        return render(
            request,
            "respondent_investment.html",
            {
                "respondent": investment.respondent,
                "invested": investment.user_investment,
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

        # TODO: Some comments explaining this logic would be helpful...
        user_received = respondent_investment
        user_bonus = 0
        if abs(respondent_investment - respondent_investment_guess) <= GUESS_THRESHOLD:
            user_received += USER_BONUS_AMOUNT

        # TODO: What's the constant value here?
        user_received += 5 - investment.user_investment

        investment.respondent_investment = respondent_investment
        investment.finished_respondent_investment = datetime.datetime.now()
        investment.respondent_investment_guess = respondent_investment_guess
        investment.user_received = user_received
        investment.user_bonus = USER_BONUS_AMOUNT
        investment.reached_stage = Investment.STAGE_COMPARE
        investment.save(
            update_fields=[
                "respondent_investment",
                "finished_respondent_investment",
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
            "invested": investment.user_investment,
            "guess_returned": investment.respondent_investment_guess,
            "real_returned": investment.respondent_investment,
            "received": investment.user_received,
            "respondent": investment.respondent,
            "guess_flag": guess_flag,
            "nodata": False,
            # TODO: What's the explanation of the hard-coded value here?
            "user_left": 5 - investment.user_investment,
            "bonus": investment.user_bonus,
        }

        return render(request, "compare.html", context)

    if request.method == "POST":
        investment.reached_stage = Investment.STAGE_QUESTION_1
        investment.save(update_fields=["reached_stage"])

        return redirect(reverse("invest_game:question1"))


@require_id_session_param
@require_http_methods(["GET", "POST"])
@require_stage(Investment.STAGE_QUESTION_1)
def question1(request, id=None):
    if request.method == "GET":
        return render(request, "question1.html")

    if request.method == "POST":
        user = InvestmentGameUser.objects.get(username=id)
        investment = Investment.objects.get(user=user)

        investment.q1answer = request.POST.get("question1")
        investment.q2answer = request.POST.get("question2")
        investment.q3answer = request.POST.get("question3")
        investment.q4answer = request.POST.get("question4")
        investment.reached_stage = Investment.STAGE_QUESTION_2

        investment.save(
            update_fields=[
                "q1answer",
                "q2answer",
                "q3answer",
                "q4answer",
                "reached_stage",
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

        investment.q5answer = request.POST.get("question5")
        investment.reached_stage = Investment.STAGE_QUESTION_3

        investment.save(update_fields=["q5answer", "reached_stage"])

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

        investment.q6answer = request.POST.get("question6")
        investment.q7answer = request.POST.get("question7")
        investment.q8answer = request.POST.get("question8")
        investment.q9answer = request.POST.get("question9")
        investment.q10answer = request.POST.get("question10")
        investment.q11answer = request.POST.get("question11")
        investment.q12answer = request.POST.get("question12")
        investment.q13answer = request.POST.get("question13")
        investment.q14answer = request.POST.get("question14")
        investment.q15answer = request.POST.get("question15")
        investment.reached_stage = Investment.STAGE_FINISH

        investment.save(
            update_fields=[
                "q6answer",
                "q7answer",
                "q8answer",
                "q9answer",
                "q10answer",
                "q11answer",
                "q12answer",
                "q13answer",
                "q14answer",
                "q15answer",
                "reached_stage",
            ]
        )

        return redirect(reverse("invest_game:finish"))


@require_id_session_param
@require_GET
@require_stage(Investment.STAGE_FINISH)
def finish(request, id=None):
    request.session["id"] = None

    return render(request, "finish.html")


# TODO: What's the intended purpose of this view?
def final(request):
    if request.method == "POST":
        requestPost = json.loads(request.body.decode("utf-8"))
        if ("REMOTE_USER" in request.META and request.META["REMOTE_USER"] != "") or (
            request.session.get("umid", False) and request.session["umid"] != ""
        ):
            if "REMOTE_USER" in request.META and request.META["REMOTE_USER"] != "":
                umid = request.META["REMOTE_USER"]
            if request.session.get("umid", False) and request.session["umid"] != "":
                umid = request.session["umid"]
            if "returned" in requestPost and requestPost["returned"] != "":
                returned = int(requestPost["returned"])
                part = 7
                user = InvestmentGameUser.objects.get(username=umid)
                gameNum = 1
                if user.firstgame == "investment":
                    gameNum = 1
                elif user.secondgame == "investment":
                    gameNum = 2
                elif user.thirdgame == "investment":
                    gameNum = 3
                if user.investment_set.count() != 0:
                    investment = user.investment_set.all()[0]
                    if (
                        investment.otherreturned == -1
                        and investment.otherinvested == -1
                    ):
                        for i in range(2, part + 1):
                            if i == 2:
                                returned = investment.returned0
                            elif i == 3:
                                returned = investment.returned1
                            elif i == 4:
                                returned = investment.returned2
                            elif i == 5:
                                returned = investment.returned3
                            elif i == 6:
                                returned = investment.returned4
                            elif i == 7:
                                returned = int(requestPost["returned"])
                                investment.returned5 = returned
                                investment.startedreturned5 = datetime.datetime.strptime(
                                    request.session["started"], "%b %d %Y %I:%M:%S %p"
                                )
                                investment.finishedreturned5 = datetime.datetime.now()
                                investment.save()
                            if returned == -1:
                                part = i
                                context = {
                                    "umid": umid,
                                    "returned": returned,
                                    "part": part,
                                    "gameNum": gameNum,
                                }
                                return render(request, "games/Trust Game.html", context)

                        otherPlayer = None
                        otherPlayersComparison = Investment.objects.filter(
                            otherreturned=-1
                        ).filter(otherinvested=-1)
                        otherPlayers = (
                            Investment.objects.filter(user__version="Pilot")
                            .exclude(user=user)
                            .order_by("?")
                        )
                        for other in otherPlayers:
                            if (
                                other.invested != -1
                                and other.returned5 != -1
                                and not other in otherPlayersComparison
                            ):
                                otherPlayer = other
                                break
                        if otherPlayer == None:
                            return JsonResponse({"found": 0})
                        InvestOrReturn = random.getrandbits(1)
                        if InvestOrReturn:
                            investAmount = investment.invested
                            if investAmount == 0:
                                returnAmount = otherPlayer.returned0
                            elif investAmount == 1:
                                returnAmount = otherPlayer.returned1
                            elif investAmount == 2:
                                returnAmount = otherPlayer.returned2
                            elif investAmount == 3:
                                returnAmount = otherPlayer.returned3
                            elif investAmount == 4:
                                returnAmount = otherPlayer.returned4
                            elif investAmount == 5:
                                returnAmount = otherPlayer.returned5
                            investment.otherreturned = returnAmount
                            # otherPlayer.otherinvested = investAmount

                            investment.points = 5 - investAmount + returnAmount
                            # otherPlayer.points = 5 + (3 * investAmount) - returnAmount

                        else:
                            investAmount = otherPlayer.invested
                            if investAmount == 0:
                                returnAmount = investment.returned0
                            elif investAmount == 1:
                                returnAmount = investment.returned1
                            elif investAmount == 2:
                                returnAmount = investment.returned2
                            elif investAmount == 3:
                                returnAmount = investment.returned3
                            elif investAmount == 4:
                                returnAmount = investment.returned4
                            elif investAmount == 5:
                                returnAmount = investment.returned5
                            # otherPlayer.otherreturned = returnAmount
                            investment.otherinvested = investAmount

                            # otherPlayer.points = 5 - investAmount + returnAmount
                            investment.points = 5 + (3 * investAmount) - returnAmount

                        investment.otheruser = otherPlayer.user
                        # otherPlayer.otheruser = user
                        investment.save()
                        # otherPlayer.save()

                        return JsonResponse(
                            {
                                "InvestOrReturn": InvestOrReturn,
                                "found": 1,
                                "returnAmount": returnAmount,
                                "investAmount": investAmount,
                                "points": investment.points,
                            }
                        )
                    else:
                        if investment.otherreturned != -1:
                            return JsonResponse(
                                {
                                    "InvestOrReturn": True,
                                    "found": 1,
                                    "returnAmount": investment.otherreturned,
                                    "investAmount": investment.invested,
                                    "points": investment.points,
                                }
                            )
                        elif investment.otherinvested != -1:
                            investAmount = investment.otherinvested
                            if investAmount == 0:
                                returnAmount = investment.returned0
                            elif investAmount == 1:
                                returnAmount = investment.returned1
                            elif investAmount == 2:
                                returnAmount = investment.returned2
                            elif investAmount == 3:
                                returnAmount = investment.returned3
                            elif investAmount == 4:
                                returnAmount = investment.returned4
                            elif investAmount == 5:
                                returnAmount = investment.returned5
                            return JsonResponse(
                                {
                                    "InvestOrReturn": False,
                                    "found": 1,
                                    "returnAmount": returnAmount,
                                    "investAmount": investAmount,
                                    "points": investment.points,
                                }
                            )
                context = {"umid": umid, "gameNum": gameNum}
                return render(request, "trust_game.html", context)

    context = {"umid": "", "welcomepage": 1}
    return render(request, "welcome.html", context)
