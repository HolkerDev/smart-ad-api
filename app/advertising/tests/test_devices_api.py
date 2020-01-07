from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Device
from advertising.serializers import DeviceSerializer

DEVICE_URL = reverse('advertising:device-list')


class PublicDeviceApiTests(TestCase):
    """Test that publicity available device api"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(DEVICE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDeviceApiTests(TestCase):
    """Test the private device api"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email='test.random@mail.com',
            password='11111'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_device_list(self):
        """Test retrieving a list of devices"""
        Device.objects.create(
            user=self.user,
            name='test.random.name'
        )
        Device.objects.create(
            user=self.user,
            name='test2.random.name'
        )
        res = self.client.get(DEVICE_URL)
        devices = Device.objects.all().order_by('-name')
        serializer = DeviceSerializer(devices, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_device_list_limited_to_user(self):
        """Test devices are shown only for authenticated user"""
        user2 = get_user_model().objects.create(
            email='test2.random@mail.com',
            password='11111'
        )
        Device.objects.create(
            user=user2,
            name='test1.random.name'
        )
        device = Device.objects.create(
            user=self.user,
            name='test2.random.name'
        )
        res = self.client.get(DEVICE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(device.name, res.data[0]['name'])

    def test_create_device_successful(self):
        """Test create a new device"""
        payload = {
            'name': 'test.random.name'
        }
        self.client.post(DEVICE_URL, payload)
        exists = Device.objects.filter(user=self.user, name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_device_invalid(self):
        """Test creating invalid device fails"""
        payload = {
            'name': ''
        }
        res = self.client.post(DEVICE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
