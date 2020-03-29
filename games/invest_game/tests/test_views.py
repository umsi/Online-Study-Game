import json

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

    def test_view_behaves_correctly_based_on_id_params(self):
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

    def test_view_behaves_correctly_based_on_current_stage(self):
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


class TestUserInvestmentView(TestCase):
    def setUp(self):
        self.current_stage_username = get_new_unqiue_username()
        self.other_stage_username = get_new_unqiue_username()
        current_stage_user = InvestmentGameUser.objects.create(
            username=self.current_stage_username
        )
        Investment.objects.create(
            user=current_stage_user, reached_stage=Investment.STAGE_USER_INVESTMENT
        )
        other_stage_user = InvestmentGameUser.objects.create(
            username=self.other_stage_username
        )
        Investment.objects.create(
            user=other_stage_user, reached_stage=Investment.STAGE_QUESTION_2
        )
        self.client = Client()

    def test_view_behaves_correctly_based_on_current_stage(self):
        set_session(self.client.session, self.other_stage_username)
        response = self.client.get("/select-respondent/")
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_QUESTION_2)
        )

        set_session(self.client.session, self.current_stage_username)
        response = self.client.get("/user-investment/")
        self.assertEqual(response.templates[0].name, "user_investment.html")

    def test_post_request_sets_the_user_investment_and_updates_the_stage(self):
        data = {"user_investment": 4}
        set_session(self.client.session, self.current_stage_username)
        response = self.client.post("/user-investment/", data)
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_RESPONDENT_INVESTMENT)
        )

        investment = Investment.objects.get(
            user=InvestmentGameUser.objects.get(username=self.current_stage_username)
        )
        self.assertEqual(investment.user_investment, 4)
        self.assertEqual(
            investment.reached_stage, Investment.STAGE_RESPONDENT_INVESTMENT,
        )


class TestRespondentInvestmentView(TestCase):
    def setUp(self):
        self.current_stage_username = get_new_unqiue_username()
        self.other_stage_username = get_new_unqiue_username()
        current_stage_user = InvestmentGameUser.objects.create(
            username=self.current_stage_username
        )
        Investment.objects.create(
            user=current_stage_user,
            reached_stage=Investment.STAGE_RESPONDENT_INVESTMENT,
            respondent="Sahal",
            user_investment=4,
        )
        other_stage_user = InvestmentGameUser.objects.create(
            username=self.other_stage_username
        )
        Investment.objects.create(
            user=other_stage_user, reached_stage=Investment.STAGE_QUESTION_2
        )
        self.client = Client()

    def test_view_behaves_correctly_based_on_current_stage(self):
        set_session(self.client.session, self.other_stage_username)
        response = self.client.get("/select-respondent/")
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_QUESTION_2)
        )

        set_session(self.client.session, self.current_stage_username)
        response = self.client.get("/respondent-investment/")
        self.assertEqual(response.templates[0].name, "respondent_investment.html")

    def test_post_request_with_bad_respondent_investment_guess(self):
        data = {"respondent_investment_guess": 6}
        set_session(self.client.session, self.current_stage_username)
        response = self.client.post("/respondent-investment/", data)
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_COMPARE)
        )

        investment = Investment.objects.get(
            user=InvestmentGameUser.objects.get(username=self.current_stage_username)
        )
        self.assertEqual(
            investment.reached_stage, Investment.STAGE_COMPARE,
        )
        # TODO: More robust testing around matching respondent investments
        # encoded in the `ans.json` file.
        self.assertEqual(investment.respondent_investment, 15)
        self.assertEqual(investment.user_bonus, 0)
        self.assertEqual(investment.user_received, 16)

    def test_post_request_with_good_respondent_investment_guess(self):
        data = {"respondent_investment_guess": 14}
        set_session(self.client.session, self.current_stage_username)
        response = self.client.post("/respondent-investment/", data)
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_COMPARE)
        )

        investment = Investment.objects.get(
            user=InvestmentGameUser.objects.get(username=self.current_stage_username)
        )
        self.assertEqual(
            investment.reached_stage, Investment.STAGE_COMPARE,
        )
        # TODO: More robust testing around matching respondent investments
        # encoded in the `ans.json` file.
        self.assertEqual(investment.respondent_investment, 15)
        self.assertEqual(investment.user_bonus, 2)
        self.assertEqual(investment.user_received, 18)


class TestCompareView(TestCase):
    def setUp(self):
        self.current_stage_username = get_new_unqiue_username()
        self.other_stage_username = get_new_unqiue_username()
        current_stage_user = InvestmentGameUser.objects.create(
            username=self.current_stage_username
        )
        Investment.objects.create(
            user=current_stage_user,
            reached_stage=Investment.STAGE_COMPARE,
            user_investment=4,
            respondent_investment_guess=6,
            respondent_investment=5,
            user_bonus=2,
            respondent="Sahal",
        )
        other_stage_user = InvestmentGameUser.objects.create(
            username=self.other_stage_username
        )
        Investment.objects.create(
            user=other_stage_user, reached_stage=Investment.STAGE_QUESTION_2
        )
        self.client = Client()

    def test_view_behaves_correctly_based_on_current_stage(self):
        set_session(self.client.session, self.other_stage_username)
        response = self.client.get("/select-respondent/")
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_QUESTION_2)
        )

        set_session(self.client.session, self.current_stage_username)
        response = self.client.get("/compare/")
        self.assertEqual(response.templates[0].name, "compare.html")

    def test_post_request_sets_the_correct_stage_and_redirects(self):
        set_session(self.client.session, self.current_stage_username)
        response = self.client.post("/compare/")
        investment = Investment.objects.get(
            user=InvestmentGameUser.objects.get(username=self.current_stage_username)
        )
        self.assertEqual(
            investment.reached_stage, Investment.STAGE_QUESTION_1,
        )
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_QUESTION_1)
        )


class TestQuestion1View(TestCase):
    def setUp(self):
        self.current_stage_username = get_new_unqiue_username()
        self.other_stage_username = get_new_unqiue_username()
        current_stage_user = InvestmentGameUser.objects.create(
            username=self.current_stage_username
        )
        Investment.objects.create(
            user=current_stage_user,
            reached_stage=Investment.STAGE_QUESTION_1,
            user_investment=4,
            respondent_investment_guess=6,
            respondent_investment=5,
            user_bonus=2,
            respondent="Sahal",
        )
        other_stage_user = InvestmentGameUser.objects.create(
            username=self.other_stage_username
        )
        Investment.objects.create(
            user=other_stage_user, reached_stage=Investment.STAGE_QUESTION_2
        )
        self.client = Client()

    def test_view_behaves_correctly_based_on_current_stage(self):
        set_session(self.client.session, self.other_stage_username)
        response = self.client.get("/question1/")

        set_session(self.client.session, self.current_stage_username)
        response = self.client.get("/question1/")
        self.assertEqual(response.templates[0].name, "question1.html")

    def test_post_request_saves_data_and_sets_stage_correctly(self):
        data = {
            "multiple_agreement_question": "exactly_3",
            "multiple_agreement_question_type": "control",
        }
        set_session(self.client.session, self.current_stage_username)
        response = self.client.post(
            "/question1/", json.dumps(data), content_type="application/json"
        )

        investment = Investment.objects.get(
            user=InvestmentGameUser.objects.get(username=self.current_stage_username)
        )
        self.assertEqual(
            investment.reached_stage, Investment.STAGE_QUESTION_2,
        )
        self.assertEqual(investment.multiple_agreement_question, "exactly_3")
        self.assertEqual(investment.multiple_agreement_question_type, "control")


class TestQuestion2View(TestCase):
    def setUp(self):
        self.current_stage_username = get_new_unqiue_username()
        self.other_stage_username = get_new_unqiue_username()
        current_stage_user = InvestmentGameUser.objects.create(
            username=self.current_stage_username
        )
        Investment.objects.create(
            user=current_stage_user, reached_stage=Investment.STAGE_QUESTION_2,
        )
        other_stage_user = InvestmentGameUser.objects.create(
            username=self.other_stage_username
        )
        Investment.objects.create(
            user=other_stage_user, reached_stage=Investment.STAGE_USER_INVESTMENT
        )
        self.client = Client()

    def test_view_behaves_correctly_based_on_current_stage(self):
        set_session(self.client.session, self.other_stage_username)
        response = self.client.get("/question2/")
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_USER_INVESTMENT)
        )

        set_session(self.client.session, self.current_stage_username)
        response = self.client.get("/question2/")
        self.assertEqual(response.templates[0].name, "question2.html")

    def test_post_request_saves_data_and_sets_stage_correctly(self):
        data = {
            "us_citizen": "no",
            "general_trustworthiness": "most_people",
            "news_source": ["cnn", "twitter", "facebook"],
            "political_views": "no_preference",
        }
        set_session(self.client.session, self.current_stage_username)
        response = self.client.post(
            "/question2/", json.dumps(data), content_type="application/json"
        )

        investment = Investment.objects.get(
            user=InvestmentGameUser.objects.get(username=self.current_stage_username)
        )
        self.assertEqual(
            investment.reached_stage, Investment.STAGE_QUESTION_3,
        )
        self.assertEqual(investment.us_citizen, "no")
        self.assertEqual(investment.general_trustworthiness, "most_people")
        self.assertEqual(investment.news_source, "['cnn', 'twitter', 'facebook']")
        self.assertEqual(investment.political_views, "no_preference")

    def test_post_request_redirects_correctly_based_on_us_citizen_answer(self):
        # Users answering yes to the U.S. citizen question should move to
        # STAGE_QUESTION_2_5.
        data = {
            "us_citizen": "yes",
            "general_trustworthiness": "most_people",
            "news_source": ["cnn", "twitter", "facebook"],
            "political_views": "no_preference",
        }
        set_session(self.client.session, self.current_stage_username)
        response = self.client.post(
            "/question2/", json.dumps(data), content_type="application/json"
        )
        investment = Investment.objects.get(
            user=InvestmentGameUser.objects.get(username=self.current_stage_username)
        )
        self.assertEqual(
            investment.reached_stage, Investment.STAGE_QUESTION_2_5,
        )

        # Reset the stage for the current user:
        investment = Investment.objects.get(
            user=InvestmentGameUser.objects.get(username=self.current_stage_username)
        )
        investment.reached_stage = Investment.STAGE_QUESTION_2
        investment.save()
        set_session(self.client.session, self.current_stage_username)

        # Users answering no to the U.S. cirizen question should move to
        # STAGE_QUESTION_3.
        data = {
            "us_citizen": "no",
            "general_trustworthiness": "most_people",
            "news_source": ["cnn", "twitter", "facebook"],
            "political_views": "no_preference",
        }
        response = self.client.post(
            "/question2/", json.dumps(data), content_type="application/json"
        )
        investment = Investment.objects.get(
            user=InvestmentGameUser.objects.get(username=self.current_stage_username)
        )
        self.assertEqual(
            investment.reached_stage, Investment.STAGE_QUESTION_3,
        )


class TestQuestion2_5View(TestCase):
    def setUp(self):
        self.current_stage_username = get_new_unqiue_username()
        self.other_stage_username = get_new_unqiue_username()
        current_stage_user = InvestmentGameUser.objects.create(
            username=self.current_stage_username
        )
        Investment.objects.create(
            user=current_stage_user, reached_stage=Investment.STAGE_QUESTION_2_5,
        )
        other_stage_user = InvestmentGameUser.objects.create(
            username=self.other_stage_username
        )
        Investment.objects.create(
            user=other_stage_user, reached_stage=Investment.STAGE_QUESTION_3
        )
        self.client = Client()

    def test_view_behaves_correctly_based_on_current_stage(self):
        set_session(self.client.session, self.other_stage_username)
        response = self.client.get("/question2-5/")
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_QUESTION_3)
        )

        set_session(self.client.session, self.current_stage_username)
        response = self.client.get("/question2-5/")
        self.assertEqual(response.templates[0].name, "question2-5.html")

    def test_post_request_saves_data_and_sets_stage_correctly(self):
        data = {
            "voted_last_election": "yes",
            "how_voted": "other",
        }
        set_session(self.client.session, self.current_stage_username)
        response = self.client.post(
            "/question2-5/", json.dumps(data), content_type="application/json"
        )

        investment = Investment.objects.get(
            user=InvestmentGameUser.objects.get(username=self.current_stage_username)
        )
        self.assertEqual(
            investment.reached_stage, Investment.STAGE_QUESTION_3,
        )
        self.assertEqual(investment.voted_last_election, "yes")
        self.assertEqual(investment.how_voted, "other")


class TestQuestion3View(TestCase):
    def setUp(self):
        self.current_stage_username = get_new_unqiue_username()
        self.other_stage_username = get_new_unqiue_username()
        current_stage_user = InvestmentGameUser.objects.create(
            username=self.current_stage_username
        )
        Investment.objects.create(
            user=current_stage_user, reached_stage=Investment.STAGE_QUESTION_3,
        )
        other_stage_user = InvestmentGameUser.objects.create(
            username=self.other_stage_username
        )
        Investment.objects.create(
            user=other_stage_user, reached_stage=Investment.STAGE_USER_INVESTMENT
        )
        self.client = Client()

    def test_view_behaves_correctly_based_on_current_stage(self):
        set_session(self.client.session, self.other_stage_username)
        response = self.client.get("/question3/")
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_USER_INVESTMENT)
        )

        set_session(self.client.session, self.current_stage_username)
        response = self.client.get("/question3/")
        self.assertEqual(response.templates[0].name, "question3.html")

    def test_post_request_saves_data_and_sets_stage_correctly(self):
        data = {
            "approve_of_trump": "approve",
            "muslims_in_neighborhood": "some",
            "muslim_coworkers": "many",
            "self_treated_unfairly": "no",
            "race_treated_unfairly": "refuse_to_answer",
            "religion_treated_unfairly": "sometimes",
            "economic_outlook": "stay_the_same",
            "islamic_extremism": "somewhat_concerned",
            "reducing_terrorism": "dont_know",
        }
        set_session(self.client.session, self.current_stage_username)
        response = self.client.post(
            "/question3/", json.dumps(data), content_type="application/json"
        )

        investment = Investment.objects.get(
            user=InvestmentGameUser.objects.get(username=self.current_stage_username)
        )
        self.assertEqual(
            investment.reached_stage, Investment.STAGE_FINISH,
        )
        self.assertEqual(investment.approve_of_trump, "approve")
        self.assertEqual(investment.muslims_in_neighborhood, "some")
        self.assertEqual(investment.muslim_coworkers, "many")
        self.assertEqual(investment.self_treated_unfairly, "no")
        self.assertEqual(investment.race_treated_unfairly, "refuse_to_answer")
        self.assertEqual(investment.religion_treated_unfairly, "sometimes")
        self.assertEqual(investment.economic_outlook, "stay_the_same")
        self.assertEqual(investment.islamic_extremism, "somewhat_concerned")
        self.assertEqual(investment.reducing_terrorism, "dont_know")


class TestFinishView(TestCase):
    def setUp(self):
        self.current_stage_username = get_new_unqiue_username()
        self.other_stage_username = get_new_unqiue_username()
        current_stage_user = InvestmentGameUser.objects.create(
            username=self.current_stage_username
        )
        Investment.objects.create(
            user=current_stage_user, reached_stage=Investment.STAGE_FINISH,
        )
        other_stage_user = InvestmentGameUser.objects.create(
            username=self.other_stage_username
        )
        Investment.objects.create(
            user=other_stage_user, reached_stage=Investment.STAGE_USER_INVESTMENT
        )
        self.client = Client()

    def test_view_behaves_correctly_based_on_current_stage(self):
        set_session(self.client.session, self.other_stage_username)
        response = self.client.get("/finish/")
        self.assertRedirects(
            response, reverse("invest_game:%s" % Investment.STAGE_USER_INVESTMENT)
        )

        set_session(self.client.session, self.current_stage_username)
        response = self.client.get("/finish/")
        self.assertEqual(response.templates[0].name, "finish.html")

    def test_view_resets_id_session_param(self):
        self.assertEqual(self.client.session.get("id"), None)
