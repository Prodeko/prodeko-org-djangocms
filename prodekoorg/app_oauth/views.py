from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import generics, permissions

from .serializers import UserSerializer


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = UserSerializer

    def get_object(self):
        model = get_user_model()
        return get_object_or_404(model, pk=self.request.user.pk)
