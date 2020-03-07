import tempfile
import os
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework import test
from PIL import Image
from rest_framework.test import APIClient
from core.models import Advertising, Device, Audience
from advertising.serializers import AdvertisingSerializer, AdvertisingDetailSerializer

ADVERTISING_URL = reverse('advertising:advertising-list')


def detail_url(advertising_id):
    """Return recipe detail URL"""
    return reverse('advertising:advertising-detail', args=[advertising_id])


def sample_advertising(user, **params):
    """Create and return a sample advertising"""
    defaults = {
        'name': 'Sample advertising',
        'seconds': 10,
        'fromDate': datetime.now(),
        'toDate': datetime.now() + timedelta(days=3),
    }
    defaults.update(params)
    return Advertising.objects.create(user=user, **defaults)


def sample_audience(name='woman'):
    """Create and return a sample audience"""
    return Audience.objects.create(name=name)


def sample_device(user, name='test.random.device'):
    """Create and return a sample device"""
    return Device.objects.create(user=user, name=name)


class PublicAdvertisingApiTest(TestCase):
    """Test unauthorized advertising API access"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(ADVERTISING_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAdvertisingApiTest(TestCase):
    """Test unauthenticated advertising API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test.random@mail.com',
            '11111'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_advertising(self):
        """Test retrieving a list of advertising"""
        sample_advertising(user=self.user)
        sample_advertising(user=self.user)

        res = self.client.get(ADVERTISING_URL)

        advertising = Advertising.objects.all()
        serializer = AdvertisingSerializer(advertising, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_advertising_limited_to_user(self):
        """Test retrieving advertising for user"""
        user2 = get_user_model().objects.create_user(
            'test2.random@mail.com',
            '11111'
        )
        sample_advertising(user=user2)
        sample_advertising(user=self.user)

        res = self.client.get(ADVERTISING_URL)

        advertising = Advertising.objects.filter(user=self.user)
        serializer = AdvertisingSerializer(advertising, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_advertising_detail(self):
        """Test viewing a advertising detail"""
        advertising = sample_advertising(user=self.user)
        advertising.devices.add(sample_device(user=self.user))
        advertising.audiences.add(sample_audience())
        url = detail_url(advertising.id)
        res = self.client.get(url)
        serializer = AdvertisingDetailSerializer(advertising)
        self.assertEqual(res.data, serializer.data)
