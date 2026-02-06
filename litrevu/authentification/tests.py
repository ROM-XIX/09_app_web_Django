# /P_09/litrevu/authentification/tests.py
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="secret123")

    def test_login_page_renders(self):
        r = self.client.get(reverse("login"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Connexion")

    def test_root_redirects_to_login_when_anonymous(self):
        r = self.client.get(reverse("root"))
        self.assertEqual(r.status_code, 302)
        self.assertIn(reverse("login"), r["Location"])

    def test_root_redirects_to_feed_when_authenticated(self):
        self.client.login(username="alice", password="secret123")
        r = self.client.get(reverse("root"))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r["Location"], reverse("feed"))

    def test_login_works_and_redirects_to_feed(self):
        r = self.client.post(
            reverse("login"),
            {"username": "alice", "password": "secret123"},
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r["Location"], reverse("feed"))
