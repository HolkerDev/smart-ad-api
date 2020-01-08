from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from secrets import token_urlsafe
from rest_framework.test import APIClient
from core.models import Device
from advertising.serializers import DeviceSerializer

ACTIVATE_URL = reverse('recognition:activate')


def sample_device(user):
    return Device.objects.create(
        user=user,
        name='test.random.name',
        key=token_urlsafe(16)
    )


class ActivateDeviceTests(TestCase):
    """Test device activation process API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email='test.random@mail.com',
            password='11111'
        )
        self.client.force_authenticate(user=self.user)

    def test_activate_device_successful(self):
        """Test activation process successful"""
        device = sample_device(self.user)

        payload = {
            'API_KEY': device.key,
            'longitude': '123.0000',
            'latitude': '124.0000'
        }

        res = self.client.get(ACTIVATE_URL, payload)
        device.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['result'], 'activated')
        self.assertTrue(device.is_active)

    def test_activate_device_invalid_params(self):
        """Test activation process with invalid params"""
        device = sample_device(self.user)
        payload = {
            'API_KEY': '',
            'longitude': '12.00',
            'latitude': '121.1241'
        }
        res = self.client.get(ACTIVATE_URL, payload)
        device.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(device.is_active)

    def test_activate_device_invalid_key(self):
        """Test activation process with invalid API KEY"""
        device = sample_device(self.user)
        payload = {
            'API_KEY': device.key + '1',
            'longitude': '115',
            'latitude': '123'
        }
        res = self.client.get(ACTIVATE_URL, payload)
        device.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(device.is_active)
