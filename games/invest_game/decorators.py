from functools import wraps

from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Investment, InvestmentGameUser


def require_stage(target_stage_name):
    def _view_wrapper(view_func):
        @wraps(view_func)
        def _arguments_wrapper(request, *args, **kwargs):
            id = request.session.get("id", None)
            user = InvestmentGameUser.objects.get(username=id)
            investment = Investment.objects.get(user=user)

            if investment.reached_stage != target_stage_name:
                # The user is trying to load an invalid stage, so we redirect
                # to the stage they should currently be viewing.
                return redirect(reverse("invest_game:%s" % investment.reached_stage))

            return view_func(request, *args, **kwargs)

        return _arguments_wrapper

    return _view_wrapper


def require_unique_id_query_param(view_func):
    """
    Require that the `id` query param not already exist in the database, so
    that if a user tries to re-take the experiment with the same id after 
    finishing they are prevented from doing so.
    """

    @wraps(view_func)
    def new_view_func(request, *args, **kwargs):
        id = request.GET.get("id", None)

        try:
            user = InvestmentGameUser.objects.get(username=id)
        except InvestmentGameUser.DoesNotExist:
            user = None

        if Investment.objects.filter(user=user).exists():
            return render(request, "error.html")

        return view_func(request, *args, **kwargs)

    return new_view_func


def disallow_id_session_param(view_func):
    """
    Check if the `request.session['id']` property exists, and disallow further view
    processing if it does. Instead, route to the expected stage.
    """

    @wraps(view_func)
    def new_view_func(request, *args, **kwargs):
        id = request.session.get("id", None)

        if id is not None:
            user = InvestmentGameUser.objects.get(username=id)
            investment = Investment.objects.get(user=user)

            return redirect(reverse("invest_game:%s" % investment.reached_stage))

        return view_func(request, *args, **kwargs)

    return new_view_func
