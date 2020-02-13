from django.test import TestCase, Client
from django.urls import reverse

from ..models import Investment, InvestmentGameUser


def reset_session_id_param(session):
    session["id"] = None
    session.save()


class TestWelcomeView(TestCase):
    def setUp(self):
        user = InvestmentGameUser.objects.create(username="abcde12345")
        Investment.objects.create(user=user, reached_stage=Investment.STAGE_QUESTION_1)
        self.client = Client()

    def test_welcome_view_should_behave_correctly_based_on_id_params(self):
        """
        Test that the `welcome` view renders the welcome template if and only if
        a unique id query param is supplied and no id session param is present.

        If an id session param is present, the user should be redirected to the
        appropriate experiment stage.

        If no session id param is present but a duplicate id query param is 
        present, the user should be shown the error template.
        """

        # A unique id query param with no id session param should render the
        # welcome template.
        response = self.client.get("/", {"id": "abc123"})
        self.assertEqual(len(response.templates), 2)
        self.assertEqual(response.templates[0].name, "welcome.html")

        # A duplicate id query param with no id session param should render the
        # error template.
        reset_session_id_param(self.client.session)
        response = self.client.get("/", {"id": "abcde12345"})
        self.assertEqual(len(response.templates), 2)
        self.assertEqual(response.templates[0].name, "error.html")

        # A request to the `welcome` view with no id or session query param
        # should render the error template.
        reset_session_id_param(self.client.session)
        response = self.client.get("/", {})
        self.assertEqual(len(response.templates), 2)
        self.assertEqual(response.templates[0].name, "error.html")

        # An id session param matching an existing record, along with an
        # arbitrary id query param, should redirect to the stage view
        # corresponding to the session id param's `Investment` model.
        session = self.client.session
        session["id"] = "abcde12345"
        session.save()
        response = self.client.get("/", {"id": "xyz789"})
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_QUESTION_1)
        )

        # An id session param matching an existing record, with no id query
        # param, should also redirect to  the stage view corresponding to the
        # session id param's `Investment` model.
        session = self.client.session
        session["id"] = "abcde12345"
        session.save()
        response = self.client.get("/", {})
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_QUESTION_1)
        )

        # An id session param *not* matching an existing record, along with an
        # arbitrary id query param, should render the error page.
        session = self.client.session
        session["id"] = "wxyz1234"
        session.save()
        response = self.client.get("/", {"id": "xxxyyyzzz"})
        self.assertEqual(len(response.templates), 2)
        self.assertEqual(response.templates[0].name, "error.html")
