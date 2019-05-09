# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django imports
from django.db import models
from django.contrib.postgres.fields import JSONField


class Graph(models.Model):
    title = models.CharField(max_length=50, unique=True)


class Node(models.Model):
    nod_id = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    position = JSONField()
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE)


class Edge(models.Model):
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='source')
    target = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='target')
    weight = models.FloatField()
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
