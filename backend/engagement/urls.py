from django.conf.urls import patterns, url
from rest_framework import routers
from views import ProjectViewSet


urlpatterns = patterns('',
    url(r'home/$', 'engagement.views.home', name='home'),
)


