from functools import wraps

from django.shortcuts import render


def require_id_session_param(view_func):
    """
    Check the `request.session['id']` property to see if the current user is 
    a returning user. If not, route to an error page since we cannot proceed 
    without a `id` to uniquely identify users. If so, pass the id as a kwarg to
    the wrapped view.
    """

    @wraps(view_func)
    def new_view_func(request, *args, **kwargs):
        id = request.session.get("id", None)

        if id is None:
            return render(request, "error.html")

        kwargs["id"] = id
        response = view_func(request, *args, **kwargs)

        return response

    return new_view_func


def require_id_query_param(view_func):
    """
    Require that the wrapped view be called with an `id` query param, which we 
    assume to be uniquely set by an external link.
    """

    @wraps(view_func)
    def new_view_func(request, *args, **kwargs):
        id = request.GET.get("id", None)

        if id is None:
            return render(request, "error.html")

        kwargs["id"] = id

        return view_func(request, *args, **kwargs)

    return new_view_func
