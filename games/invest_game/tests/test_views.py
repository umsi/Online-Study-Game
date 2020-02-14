from django.test import TestCase, Client
from django.urls import reverse
from django.utils.crypto import get_random_string

from ..models import Investment, InvestmentGameUser


def set_session(session, id):
    session["id"] = id
    session.save()


def get_new_unqiue_username():
    return get_random_string()


class TestWelcomeView(TestCase):
    def setUp(self):
        self.existing_username = get_new_unqiue_username()
        user = InvestmentGameUser.objects.create(username=self.existing_username)
        Investment.objects.create(user=user, reached_stage=Investment.STAGE_QUESTION_1)
        self.client = Client()

    def test_welcome_view_behaves_correctly_based_on_id_params(self):
        """
        Test that the `welcome` view renders the welcome template if and only if
        a unique id query param is supplied and no id session param is present.

        If an id session param is present, the user should be redirected to the
        appropriate experiment stage.

        If no session id param is present but a duplicate id query param is 
        present, the user should be shown the error template.
        """

        # A unique id query param with no id session param should render the
        # welcome template and create InvestmentGameUser and Investment
        # objects with the correct username.
        response = self.client.get("/", {"id": "abc123"})
        self.assertEqual(response.templates[0].name, "welcome.html")
        self.assertEqual(
            InvestmentGameUser.objects.filter(username="abc123").count(), 1
        )
        self.assertEqual(
            Investment.objects.filter(
                user=InvestmentGameUser.objects.get(username="abc123")
            ).count(),
            1,
        )

        # Check if the next experiment stage is correctly set.
        investment = Investment.objects.get(
            user=InvestmentGameUser.objects.get(username="abc123")
        )
        self.assertEqual(
            investment.reached_stage, Investment.STAGE_SELECT_RESPONDENT,
        )

        # A duplicate id query param with no id session param should render the
        # error template.
        set_session(self.client.session, None)
        response = self.client.get("/", {"id": self.existing_username})
        self.assertEqual(response.templates[0].name, "error.html")

        # A request to the `welcome` view with no id or session query param
        # should render the error template.
        set_session(self.client.session, None)
        response = self.client.get("/", {})
        self.assertEqual(response.templates[0].name, "error.html")

        # An id session param matching an existing record, along with an
        # arbitrary id query param, should redirect to the stage view
        # corresponding to the session id param's `Investment` model.
        set_session(self.client.session, self.existing_username)
        response = self.client.get("/", {"id": get_new_unqiue_username()})
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_QUESTION_1)
        )

        # An id session param matching an existing record, with no id query
        # param, should also redirect to the stage view corresponding to the
        # session id param's `Investment` model.
        set_session(self.client.session, self.existing_username)
        response = self.client.get("/", {})
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_QUESTION_1)
        )

        # An id session param *not* matching an existing record, along with an
        # arbitrary id query param, should render the error page.
        set_session(self.client.session, get_new_unqiue_username())
        response = self.client.get("/", {"id": get_new_unqiue_username()})
        self.assertEqual(response.templates[0].name, "error.html")


class TestSelectRespondentView(TestCase):
    def setUp(self):
        self.current_stage_username = get_new_unqiue_username()
        self.other_stage_username = get_new_unqiue_username()
        current_stage_user = InvestmentGameUser.objects.create(
            username=self.current_stage_username
        )
        Investment.objects.create(
            user=current_stage_user, reached_stage=Investment.STAGE_SELECT_RESPONDENT
        )
        other_stage_user = InvestmentGameUser.objects.create(
            username=self.other_stage_username
        )
        Investment.objects.create(
            user=other_stage_user, reached_stage=Investment.STAGE_QUESTION_2
        )
        self.client = Client()

    def test_select_respondent_view_behaves_correctly_based_on_current_stage(self):
        # The view should *not* render the select_respondent.html template if
        # the stage is not STAGE_SELECT_RESPONDENT, and should instead redirect
        # to the correct stage.
        set_session(self.client.session, self.other_stage_username)
        response = self.client.get("/select-respondent/")
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_QUESTION_2)
        )

        # The view *should* render the select_respondent.html template if the
        # stage is STAGE_SELECT_RESPONDENT.
        set_session(self.client.session, self.current_stage_username)
        response = self.client.get("/select-respondent/")
        self.assertEqual(response.templates[0].name, "select_respondent.html")

    def test_post_request_sets_the_respondent_and_updates_the_stage(self):
        data = {"respondent": "Sahr"}
        set_session(self.client.session, self.current_stage_username)
        response = self.client.post("/select-respondent/", data)
        self.assertEquals(response.content.decode("utf-8"), "Sahr")

        investment = Investment.objects.get(
            user=InvestmentGameUser.objects.get(username=self.current_stage_username)
        )
        self.assertEqual(
            investment.respondent, "Sahr",
        )
        self.assertEqual(
            investment.reached_stage, Investment.STAGE_USER_INVESTMENT,
        )
