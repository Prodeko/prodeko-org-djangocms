from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from .views import (EhdokasDeleteView, EhdokasUpdateView, delete_kysymys_view,
                    main_view, update_kysymys_view)

app_name = 'app_vaalit'
urlpatterns = [
    url(r'^elections/', main_view, name='vaalit'),
    url(r'^elections/delete-question/(?P<pk>\d+)/', login_required(delete_kysymys_view), name='delete_kysymys'),
    url(r'^elections/update-question/(?P<pk>\d+)/', login_required(update_kysymys_view), name='update_kysymys'),
    url(r'^elections/delete-nominee/(?P<pk>\d+)/', login_required(EhdokasDeleteView.as_view()), name='delete_ehdokas'),
    url(r'^elections/update-nominee/(?P<pk>\d+)/', login_required(EhdokasUpdateView.as_view()), name='update_ehdokas'),
]
