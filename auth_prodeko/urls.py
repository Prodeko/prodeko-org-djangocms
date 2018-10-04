from django.conf.urls import url
from django.contrib.auth import views as auth_views

app_name = 'auth_prodeko'
urlpatterns = [
    url(r'^login/', auth_views.login, {'template_name': 'prodeko_login.html'}, name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^password_change/', auth_views.password_change, name='password_change'),
    url(r'^password_change/done/', auth_views.password_change_done, name='password_change_done'),
    url(r'^password_reset/', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/<uidb64>/<token>/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/', auth_views.password_reset_complete, name='password_reset_complete')
]