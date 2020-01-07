from rest_framework import serializers
from core.models import Advertising, Audience, Device


class DeviceSerializer(serializers.ModelSerializer):
    """Serialize an device object"""

    class Meta:
        model = Device
        fields = ('id', 'name', 'is_active', 'key')
        read_only_fields = ('id', 'key', 'is_active')


class AudienceSerializer(serializers.ModelSerializer):
    """Serialize an audience object"""

    class Meta:
        model = Audience
        fields = ('id', 'name')
        read_only_fields = ('id',)


class AdvertisingSerializer(serializers.ModelSerializer):
    """Serialize an advertising object"""
    devices = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Device.objects.all()
    )
    audiences = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Audience.objects.all()
    )

    class Meta:
        model = Advertising
        fields = ('id', 'name', 'devices', 'audiences', 'fromDate', 'toDate', 'seconds')
        read_only_fields = ('id',)


class AdvertisingImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images for advertising"""

    class Meta:
        model = Advertising
        fields = ('id', 'image')
        read_only_fields = ('id',)


class AdvertisingDetailSerializer(AdvertisingSerializer):
    """Serialize a advertising detail"""
    devices = DeviceSerializer(many=True, read_only=True)
    audiences = AudienceSerializer(many=True, read_only=True)
