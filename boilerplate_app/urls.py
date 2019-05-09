#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django imports.
from django.conf.urls import url

# local imports.
from boilerplate_app.views import GraphListCreateAPIView, GraphDetailUpdateDeleteAPIView, GraphWeaklyConnectedNodeAPIView, ParseNodeCSVAPIView, GraphListIslandsAPIView,GetOverlapNodesAPIView
from boilerplate_app.swagger import schema_view


urlpatterns = [
    url(r'^graph/$', GraphListCreateAPIView.as_view(), name='graph-list-create-api'),
    url(r'^graph/(?P<title>\w+)/$', GraphDetailUpdateDeleteAPIView.as_view(), name='graph-detail-update-delete-api'),
    url(r'^weakly_connected_nodes/(?P<title>\w+)/$', GraphWeaklyConnectedNodeAPIView.as_view(), name='graph-weekly-connected-node-api'),
    url(r'^parse_node_csv/(?P<title>\w+)/$', ParseNodeCSVAPIView.as_view(), name='parse-node-csv-api'),
    url(r'^islands/(?P<title>\w+)/$', GraphListIslandsAPIView.as_view(), name='graph-list-islands'),
    url(r'^get_overlap_node/(?P<title>\w+)/$', GetOverlapNodesAPIView.as_view(), name='graph-overlaps-api'),
    url(r'^docs/$', schema_view, name="schema_view"),

]