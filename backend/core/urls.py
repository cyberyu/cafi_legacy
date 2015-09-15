from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'core.views.main', name='landing_page'),
    url(r'login/$', 'core.views.user_login', name='login'),
    url(r'logout/$', 'core.views.user_logout', name='logout'),
    url(r'me/$', 'core.views.me', name='me'),
    url(r'^register/$', 'core.views.register', name='register'),
)
