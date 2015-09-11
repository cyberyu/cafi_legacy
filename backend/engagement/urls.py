from django.conf.urls import patterns, url
from rest_framework import routers
from views import ProjectViewSet


urlpatterns = patterns('',
    url(r'home/$', 'engagement.views.home', name='home'),
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'projects', ProjectViewSet)

urlpatterns += router.urls