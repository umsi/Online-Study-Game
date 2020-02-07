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
