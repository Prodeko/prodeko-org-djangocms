from django.conf.urls import url
from django.contrib.auth import views as auth_views

app_name = 'auth_prodeko'
urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'prodeko_login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^logout/$', auth_views.logout, name='logout')
]