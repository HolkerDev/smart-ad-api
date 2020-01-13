from rest_framework.views import APIView
from core.models import Device, Advertising
from PIL import Image
from utils.predictor import GlassesPredictor, GenderPredictor
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
import cv2


@api_view(['GET'])
def activate_device(request):
    """View for activating a new device"""
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


@api_view(['GET'])
def recognize_person(request):
    """View for face recognition"""
    api_key = request.query_params.get('API_KEY')
    image = request.FILES.get('image')
    device = get_object_or_404(Device, key=api_key)

    if image and device.is_active:
        print("Image is correct")
        up_file = request.FILES['image']
        destination = open('/tmp/' + up_file.name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        destination.close()
        print(destination.name)

        # init predictors
        predictor_glasses = GlassesPredictor()
        predictor_genders = GenderPredictor()

        # predict
        gender_result = predictor_genders.predict(destination.name)
        glasses_result = predictor_glasses.predict(destination.name)

        response = {
            "glasses": glasses_result,
            "gender": gender_result
        }
        advertising = Advertising.objects.all().filter(devices__in=[device.id])
        if advertising:
            print(f"found advertising {advertising[0].image}")
            return Response(data={"response": f"127.0.0.1:8000/media/{advertising[0].image}"},
                            status=status.HTTP_200_OK)
        else:
            return Response(data={"response": f"127.0.0.1:8000/media/default/here_your_ad.jpg"},
                            status=status.HTTP_200_OK)
