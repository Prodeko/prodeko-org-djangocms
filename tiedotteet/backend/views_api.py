from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from tiedotteet.backend.models import Category, Message, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["title"]


class MessageSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tags = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_tags(self, message):
        queryset = message.tags.all()
        return queryset.values_list("title", flat=True)

    def get_is_new(self, message):
        return message.is_new()


class CategorySerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "title", "order", "messages"]

    def get_messages(self, category):
        queryset = Message.visible_objects.filter(category=category)
        serializer = MessageSerializer(queryset, many=True)
        return serializer.data


class ContentList(APIView):
    def get(self, request, format=None):
        queryset = Category.objects.all().order_by("order")
        if not request.user.is_authenticated:
            queryset = queryset.exclude(login_required=True)
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
