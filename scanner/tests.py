from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class WebShieldTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="SafeTestPass927!"
        )

    def test_home_redirects_when_logged_out(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_home_loads_when_logged_in(self):
        self.client.login(
            username="testuser",
            password="SafeTestPass927!"
        )
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
