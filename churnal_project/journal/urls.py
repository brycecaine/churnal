from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^setpath$', views.setpath, name='setpath'),
    url(r'^timeline$', views.timeline, name='timeline'),
    url(r'^day/(?P<day>.+)$', views.day, name='day'),
]