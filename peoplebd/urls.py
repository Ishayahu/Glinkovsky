from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'user/$', views.profile, name='profile'),
    url(r'create_profile/$', views.create_profile),
    url(r'$', views.index, name='index'),

]
