# -*- coding:utf-8 -*-
# coding=<utf8>
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'user/$', views.profile),
    url(r'user/(\d+)/$', views.profile),
    url(r'user/(\d+)/(\d{4})/(\d{1,2})/$', views.profile),
    url(r'create_profile/$', views.create_profile),
    url(r'delete_profile/(\d+)/$', views.delete_profile),
    url(r'$', views.index, name='index'),

]
