from django.conf.urls import url
from health_monitor import views


urlpatterns = [
    url(r'^health/(?P<uid>[\d]*)/$', views.read, name='read'),
    url(r'^health/(?P<uid>[\d]*)/update/(?P<test_name>[\w-]*)/$', views.update, name='update'),
    url(r'^health/(?P<uid>[\d]*)/history/(?P<group>[\w-]*)/$', views.history, name='history'),
]
