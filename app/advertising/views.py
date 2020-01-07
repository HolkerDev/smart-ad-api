from rest_framework.decorators import action
import secrets
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Device, Audience, Advertising
from advertising import serializers


class DeviceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage devices in the database"""
    queryset = Device.objects.all()
    serializer_class = serializers.DeviceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, key=secrets.token_urlsafe(16))


class AudienceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage audiences in the database"""
    queryset = Audience.objects.all()
    serializer_class = serializers.AudienceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.order_by('-name')

    def perform_create(self, serializer):
        serializer.save()


class AdvertisingViewSet(viewsets.ModelViewSet):
    """Manage advertising in the database"""
    serializer_class = serializers.AdvertisingSerializer
    queryset = Advertising.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.AdvertisingDetailSerializer
        if self.action == 'upload_image':
            return serializers.AdvertisingImageSerializer
        return self.serializer_class

    def get_queryset(self):
        """Retrieve the advertising for the authenticated user"""
        devices = self.request.query_params.get('devices')
        audiences = self.request.query_params.get('audiences')
        queryset = self.queryset
        if devices:
            devices_ids = self._params_to_ints(devices)
            queryset = queryset.filter(tags__id__in=devices)
        if audiences:
            audiences_ids = self._params_to_ints(audiences)
            queryset = queryset.filter(ingredients__id__in=audiences_ids)

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to an advertising"""
        advertising = self.get_object()
        serializer = self.get_serializer(
            advertising,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
