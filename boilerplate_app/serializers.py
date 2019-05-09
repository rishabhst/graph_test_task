#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django imports.
from django.db import transaction

# Rest Framework imports.
from rest_framework import serializers

# Third Party Library imports

# local imports.
from boilerplate_app.models import Graph, Node, Edge

class GraphSerializer(serializers.ModelSerializer):
    nodes = serializers.SerializerMethodField()
    edges = serializers.SerializerMethodField()

    class Meta:
        model = Graph
        fields = ('title', 'nodes', 'edges')

    def get_nodes(self, object):
        node_list = []
        nodes = object.node_set.all()
        for node in nodes:
            node_list.append({'id':node.nod_id, 'title':node.title, 'position':node.position}) 
        return node_list

    def get_edges(self, object):
        edge_list = []
        edges = object.edge_set.all()
        for edge in edges:
            edge_list.append({'source':edge.source.nod_id, 'target':edge.target.nod_id, 'weight':edge.weight}) 
        return edge_list


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        exclude = ('graph',)