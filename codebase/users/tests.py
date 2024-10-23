from django.test import TestCase

from .models import User


class TestUserModel(TestCase):
    def setUp(self):
        self.username, self.user_email = "testuser", "test@example.com"
        self.user_obj = User.objects.create(username=self.username, email=self.user_email, password="1234")

    def test_dunder_str_of_user(self):
        self.assertEqual(str(self.user_obj), f"{self.username} | {self.user_email}")

    def test_delete_account_url_of_user(self):
        self.assertIn("delete", self.user_obj.delete_account_url)
