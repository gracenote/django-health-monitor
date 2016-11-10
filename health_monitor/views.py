# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	snapshot,
)


class snapshotCreateView(CreateView):

    model = snapshot


class snapshotDeleteView(DeleteView):

    model = snapshot


class snapshotDetailView(DetailView):

    model = snapshot


class snapshotUpdateView(UpdateView):

    model = snapshot


class snapshotListView(ListView):

    model = snapshot

