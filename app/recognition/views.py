from rest_framework.views import APIView
from core.models import Device
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def activate_device(request):
    api_key = request.query_params.get('API_KEY')
    longitude = request.query_params.get('longitude')
    latitude = request.query_params.get('latitude')

    if api_key and longitude and latitude:

        device = get_object_or_404(Device, key=api_key)

        device.longitude = longitude
        device.latitude = latitude
        device.is_active = True

        device.save()
        return Response({'result': 'activated'})
    else:
        return Response({'detail': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
