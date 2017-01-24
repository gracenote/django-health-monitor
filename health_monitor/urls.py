from django.conf.urls import url
from health_monitor import views


urlpatterns = [
    url(r'^health/(?P<uid>[\w-]*)/$', views.read, name='read'),
    url(r'^health/(?P<uid>[\w-]*)/update/(?P<test_name>[\w-]*)/$', views.update, name='update'),
    url(r'^health/(?P<uid>[\w-]*)/history/(?P<subscriber>[\w-]*)/$', views.history, name='history'),
]
