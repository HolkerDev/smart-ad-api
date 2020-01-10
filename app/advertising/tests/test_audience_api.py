from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Audience

from advertising.serializers import AudienceSerializer

AUDIENCE_URL = reverse("advertising:audience-list")


class PublicAudienceApiTests(TestCase):
    """Test that publicity is available"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving audiences"""
        res = self.client.get(AUDIENCE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAudienceApiTests(TestCase):
    """Test the authorized user tags api"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email='test.random@mail.com',
            password='11111'
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_audiences(self):
        """Test retrieving audiences"""
        Audience.objects.create(name='woman')
        Audience.objects.create(name='man')

        res = self.client.get(AUDIENCE_URL)
        audience = Audience.objects.all().order_by('-name')
        serializer = AudienceSerializer(audience, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_audience_successful(self):
        """Test create the audience"""
        payload = {
            'name': 'woman'
        }
        res = self.client.post(AUDIENCE_URL, payload)
        exists = Audience.objects.filter(
            name=payload['name']
        ).exists()
        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_audience_invalid(self):
        """Test creating a new audience with invalid payload"""
        payload = {
            'name': ''
        }
        res = self.client.post(AUDIENCE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
