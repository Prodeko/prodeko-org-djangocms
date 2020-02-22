from rest_framework import serializers

from alumnirekisteri.auth2.models import User
from alumnirekisteri.rekisteri.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")


class PersonSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Person
        fields = "__all__"
