"""
   Copyright 2017 Gracenote

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^health/$', views.BodyHealthView.as_view()),
    url(r'^health/(?P<uid>[\w]*)/$', views.BodyHealthView.as_view()),
    url(r'^health/(?P<uid>[\w]*)/(?P<group>[\w]*)/$', views.BodyHealthView.as_view()),
    url(r'^health/(?P<uid>[\w]*)/(?P<group>[\w]*)/(?P<test>[\w]*)/$', views.BodyHealthView.as_view()),
    url(r'^health_test/$', views.BodyHealthTestView.as_view()),
    url(r'^health_test/(?P<test>[\w-]*)/$', views.BodyHealthTestView.as_view()),
    url(r'^health_test/(?P<test>[\w-]*)/(?P<uid>[\d]*)/$', views.BodyHealthTestView.as_view()),
]
