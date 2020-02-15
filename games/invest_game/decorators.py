from functools import wraps

from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Investment, InvestmentGameUser


def require_stage(target_stage_name):
    """
    Require that the value of `reached_stage` on the `Investment` model
    corresponding to the current session be equivalent to the stage declared
    when this decorator is invoked. If `reached_stage` matches the declared
    stage, allow further processing of the view. If not, redirect to the
    correct stage.
    """

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


def require_unique_id_query_param_and_disallow_id_session_param(view_func):
    """
    Require that the `id` query param exist and not already correspond to a
    record in the database, and furthermore disallow an existing id session 
    param. In other words, only allow further view processing if a unique id 
    query param is supplied and no id session param already exists.
    """

    @wraps(view_func)
    def new_view_func(request, *args, **kwargs):
        session_id = request.session.get("id", None)
        id = request.GET.get("id", None)

        if session_id is not None:
            # If a session token already exists and has an `id` parameter, the
            # user is attempting to restart the experiment. In that case,
            # redirect to the stage they *should* be on.
            try:
                user = InvestmentGameUser.objects.get(username=session_id)
                investment = Investment.objects.get(user=user)
            except (InvestmentGameUser.DoesNotExist, Investment.DoesNotExist) as e:
                return render(request, "error.html")

            return redirect(reverse("invest_game:%s" % investment.reached_stage))

        elif session_id is None and id is None:
            # If no query id param or session id param exists, render the error
            # page.
            return render(request, "error.html")

        elif id is not None and session_id is None:
            # If we have an id query param and no session id param, check to
            # make sure the id query param is not a duplicate. We might have a
            # duplicate if a user finishes the study (and in so doing clears
            # their session id param), and then for some reason restarts the
            # study using the same id query param they originally used. In this
            # case we want to show the error page.
            try:
                user = InvestmentGameUser.objects.get(username=id)
            except InvestmentGameUser.DoesNotExist:
                kwargs["id"] = id
                return view_func(request, *args, **kwargs)

            try:
                investment = Investment.objects.get(user=user)
            except Investment.DoesNotExist:
                kwargs["id"] = id
                return view_func(request, *args, **kwargs)

        return render(request, "error.html")

    return new_view_func
