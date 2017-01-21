from django.conf.urls import url
from health_monitor import views


urlpatterns = [
    url(r'^(?P<uid>[\w-]*)/$', views.read, name='read'),
    url(r'^(?P<uid>[\w-]*)/history/(?P<subscriber>[\w-]*)/$', views.history, name='history'),
    url(r'^(?P<uid>[\w-]*)/update/(?P<test_name>[\w-]*)/$', views.update, name='update'),
]
