from rest_framework import generics, permissions, filters
from alumnirekisteri.rekisteri.models import *
from alumnirekisteri.auth2.models import User
from alumnirekisteri.rekisteri.serializers import *


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PersonList(generics.ListAPIView):
    """ Read only. Serialize a list of persons. """

    serializer_class = PersonSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """ Filter queryset against GET-parameters """
        queryset = Person.objects.all()
        first_name = self.request.query_params.get("firstname", None)
        if first_name is not None:
            queryset = queryset.filter(user__first_name=first_name)
        last_name = self.request.query_params.get("lastname", None)
        if last_name is not None:
            queryset = queryset.filter(user__last_name=last_name)
        class_of_year = self.request.query_params.get("year", None)
        if class_of_year is not None and class_of_year.isdigit():
            queryset = queryset.filter(class_of_year=class_of_year)
        return queryset


class PersonDetail(generics.RetrieveAPIView):
    """ Read only. Serialize one person. """

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = (permissions.IsAuthenticated,)
