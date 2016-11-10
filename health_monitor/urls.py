# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(
        regex="^snapshot/~create/$",
        view=views.snapshotCreateView.as_view(),
        name='snapshot_create',
    ),
    url(
        regex="^snapshot/(?P<pk>\d+)/~delete/$",
        view=views.snapshotDeleteView.as_view(),
        name='snapshot_delete',
    ),
    url(
        regex="^snapshot/(?P<pk>\d+)/$",
        view=views.snapshotDetailView.as_view(),
        name='snapshot_detail',
    ),
    url(
        regex="^snapshot/(?P<pk>\d+)/~update/$",
        view=views.snapshotUpdateView.as_view(),
        name='snapshot_update',
    ),
    url(
        regex="^snapshot/$",
        view=views.snapshotListView.as_view(),
        name='snapshot_list',
    ),
	]
