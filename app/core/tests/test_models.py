import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from .. import models
from unittest.mock import patch


def sample_user(email='test.random@mail.com', password='11111'):
    """Creates a sample user"""
    return get_user_model().objects.create_user(email=email, password=password)


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
        self.assertTrue(user.is_staff, True)

    def test_device_str(self):
        """Test device string representation"""
        device = models.Device.objects.create(
            user=sample_user(),
            name='test.random.name'
        )
        self.assertEqual(str(device), device.name)

    def test_audience_str(self):
        """Test audience string representation"""
        audience = models.Audience.objects.create(
            name='test.random.name'
        )
        self.assertEqual(str(audience), audience.name)

    def test_advertising_str(self):
        """Test advertising string representation"""
        advertising = models.Advertising.objects.create(
            user=sample_user(),
            name='test.random.name',
            seconds=10,
            fromDate=datetime.datetime.now(),
            toDate=datetime.datetime.now().day + 3
        )
        self.assertEqual(str(advertising), advertising.name)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        filepath = models.advertising_image_file_path(None, 'test.random.name.jpg')

        exp_path = f'uploads/advertising/{uuid}.jpg'
        self.assertEqual(filepath, exp_path)
