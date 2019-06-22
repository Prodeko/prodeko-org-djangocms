from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Slide


class SlideSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Slide
        fields = ["id", "title", "description", "highlight", "is_active"]

    def get_is_active(self, slide):
        return slide.is_active()


class SlidesList(APIView):
    """ List all slides """

    def get(self, request, format=None):
        queryset = Slide.objects.all().order_by("-start_datetime")
        serializer = SlideSerializer(queryset, many=True)
        return Response(serializer.data)
