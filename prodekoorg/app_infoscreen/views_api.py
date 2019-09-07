import datetime
import json

from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Slide


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ["id", "title", "description", "highlight", "image"]


class SlidesList(APIView):
    """ List all slides """

    def get(self, request, format=None):
        queryset = Slide.objects.all().order_by("-start_datetime")
        active_slides = [s for s in queryset if s.is_active()]
        serializer = SlideSerializer(active_slides, many=True)
        return Response(serializer.data)


def now(request):
    """ Return current time"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(json.dumps(now), content_type="application/json")
