from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Slide


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = "__all__"


class SlidesList(APIView):
    """ List all slides """

    def get(self, request, format=None):
        queryset = Slide.objects.all().order_by("-start_datetime")
        serializer = SlideSerializer(queryset, many=True)
        return Response(serializer.data)
