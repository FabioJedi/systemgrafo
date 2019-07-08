# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.conf.urls import url
from .views import GeneListView, GeneDetailView, ProteinListView, ProteinDetailView, index

urlpatterns = [
    # Index view
    url(r'^$', index),
    url(r'^genes/$', GeneListView.as_view(), name='gene-list'),
    url(r'^genes/(?P<pk>[\d]+)/$', GeneDetailView.as_view(), name='gene-detail'),
    url(r'^proteins/$', ProteinListView.as_view(), name='protein-list'),
    url(r'^proteins/(?P<pk>[\d]+)/$', ProteinDetailView.as_view(), name='protein-detail'),
]
