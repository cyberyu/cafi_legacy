from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'core.views.main', name='landing_page'),
    url(r'login/$', 'core.views.user_login', name='login'),
    url(r'^register/$', 'core.views.register', name='register'),
    url(r'^user/profile/$', 'core.views.user_profile', name='user_profile'),
    url(r'^user/searches/$', 'core.views.past_searches', name='user_searches'),
)
