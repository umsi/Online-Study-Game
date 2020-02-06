from django.urls import path
from django.contrib import admin

from . import views


app_name = "invest_game"
urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("sign-in/", views.sign_in, name="sign_in"),
    path("select-respondent/", views.select_respondent, name="select_respondent"),
    path("user-investment/", views.user_investment, name="user_investment"),
    path(
        "respondent-investment/",
        views.respondent_investment,
        name="respondent_investment",
    ),
    path("final/", views.final, name="final"),
    path("compare/", views.compare, name="compare"),
    path("question1/", views.question1, name="question1"),
    path("question2/", views.question2, name="question2"),
    path("question3/", views.question3, name="question3"),
    path("finish/", views.finish, name="finish"),
]
