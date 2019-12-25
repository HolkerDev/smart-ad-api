from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_succ(self):
        """Test creating a new user with an email succesfully"""
        email = 'holest.test@gmail.com'
        password = 'testpass12'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@GMAIL.com"
        user = get_user_model().objects.create_user(email, "123141231")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '1243user')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser("haron.dev@gmail1.2com", "1234")
        self.assertTrue(user.is_superuser, True)
        self.assertTrue(user.is_stuff, True)
