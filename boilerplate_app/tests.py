# from model_mommy import mommy
# from django.test import TestCase


# from rest_framework_jwt.serializers import JSONWebTokenSerializer


# from boilerplate_app.models import User
# from boilerplate_app.serializers import UserListSerializer, UserCreateSerializer


# class APITests(TestCase):

#     def test_list_user(self):

#         user = mommy.make(User)
#         self.assertTrue(isinstance(user, User))

#         user_serializer = UserListSerializer(user)

#         assert user.id == user_serializer.data.get('id')
#         assert user.first_name == user_serializer.data.get('first_name')
#         assert user.last_name == user_serializer.data.get('last_name')
#         assert user.email == user_serializer.data.get('email')
#         assert user.role == user_serializer.data.get('role')

#     def test_register(self):

#         request_data = {
#             "username": "username",
#             "first_name" : "first_name",
#             "last_name" : "last_name",
#             "email" : "email@gmail.com",
#             "password" : "qwerty1234",
#             "role" : "role"
#         }
#         user_serializer = UserCreateSerializer(data=request_data)
#         if user_serializer.is_valid():
#             pass
#         else:
#             message = ''
#             for error in user_serializer.errors.values():
#                 message += " "
#                 message += error[0]
#             print(message)

#         user = User(username=request_data.get('username'), first_name=request_data.get('first_name'), last_name=request_data.get('last_name'), email=request_data.get('email'), password=request_data.get('password'), role=request_data.get('role'))

#         assert request_data.get('username') == user_serializer.data.get('username') 
#         assert request_data.get('first_name') == user_serializer.data.get('first_name')
#         assert request_data.get('last_name') == user_serializer.data.get('last_name')
#         assert request_data.get('email') == user_serializer.data.get('email')
#         assert request_data.get('role') == user_serializer.data.get('role')





# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django imports
from django.test import TestCase
from django.urls import reverse

# rest framework imports
from rest_framework.test import APIClient
from rest_framework import status

# third party imports
from django.test import mock
from unittest.mock import patch

# local imports
from boilerplate_app.models import Graph, Node, Edge


class GraphAPITestCases(TestCase):

    def setUp(self):
        self.title = "TestGraph"
        self.nod_id1, self.nod_id2  = "X1", "X2"
        self.nod_id3 = "X3"
        self.nod_id4 = "X4"
        self.nod_id5 = "X5"
        self.nod_id6 = "X6"
        self.nod_title = "XYZ1"
        self.position = {"top": 10, "left": 15, "bottom": 30, "right": 50}
        self.weight = 0.5
        self.weight1 = 0.7
        self.URLS = {
                    'graph-list-create-api': reverse('boilerplate_app-api:graph-list-create-api'),
                    'graph-detail-update-delete-api': reverse('boilerplate_app-api:graph-detail-update-delete-api', kwargs={'title': self.title}),
                    'graph-weekly-connected-node-api': reverse('boilerplate_app-api:graph-weekly-connected-node-api', kwargs={'title': self.title}),
                    'parse-node-csv-api': reverse('boilerplate_app-api:parse-node-csv-api', kwargs={'title': self.title}),
                    'graph-list-islands': reverse('boilerplate_app-api:graph-list-islands', kwargs={'title': self.title}),
                     }

    def create_graph(self):
        graph = Graph.objects.create(title=self.title)

        Node.objects.bulk_create([
            Node(nod_id=self.nod_id1, title=self.nod_title, position=self.position, graph=graph),
            Node(nod_id=self.nod_id2, title=self.nod_title, position=self.position, graph=graph),
            Node(nod_id=self.nod_id3, title=self.nod_title, position=self.position, graph=graph),
            Node(nod_id=self.nod_id4, title=self.nod_title, position=self.position, graph=graph),
            Node(nod_id=self.nod_id5, title=self.nod_title, position=self.position, graph=graph),
            Node(nod_id=self.nod_id6, title=self.nod_title, position=self.position, graph=graph)
        ])

        resp = Edge.objects.bulk_create([
            Edge(source=Node.objects.get(nod_id=self.nod_id1, graph=graph), target=Node.objects.get(nod_id=self.nod_id2, graph=graph), weight=self.weight, graph=graph),
            Edge(source=Node.objects.get(nod_id=self.nod_id1, graph=graph), target=Node.objects.get(nod_id=self.nod_id3, graph=graph), weight=self.weight1, graph=graph),
            Edge(source=Node.objects.get(nod_id=self.nod_id4, graph=graph), target=Node.objects.get(nod_id=self.nod_id5, graph=graph), weight=self.weight, graph=graph)
        ])

    def test_create_graph(self):
        client = APIClient()
        resp = client.post(self.URLS['graph-list-create-api'], {
                    "title": "TestGraph1",
                    "nodes": [
                    {
                    "id": "x1",
                    "title": "ABC",
                    "position": {"top": 10, "left": 15, "bottom": 30, "right": 50}
                    },
                    {
                    "id": "x2",
                    "title": "DEF",
                    "position": {"top": 10, "left": 60, "bottom": 30, "right": 95}
                    },
                    {
                    "id": "x3",
                    "title": "GHI",
                    "position": {"top": 10, "left": 100, "bottom": 30, "right": 125}
                    }
                    ],
                    "edges": [
                    {"source": "x1", "target": "x2", "weight": 0.5},
                    {"source": "x1", "target": "x3", "weight": 0.8}
                    ]
                }, format='json')
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data['status'] == 'created'

    def test_list_graph(self):
        client = APIClient()
        self.create_graph()

        resp = client.get(self.URLS['graph-list-create-api'])
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['Response'][0]['title'] == 'TestGraph'
        assert len(resp.data['Response'][0]['nodes']) != 0
        assert len(resp.data['Response'][0]['edges']) != 0

    def test_detail_graph(self):
        client = APIClient()
        self.create_graph()

        resp = client.get(self.URLS['graph-detail-update-delete-api'])

        assert resp.status_code == status.HTTP_200_OK 
        assert resp.data['Response']['title'] == 'TestGraph'
        assert len(resp.data['Response']['nodes']) != 0
        assert len(resp.data['Response']['edges']) != 0

    def test_update_graph(self):
        client = APIClient()
        self.create_graph()
        resp = client.put(self.URLS['graph-detail-update-delete-api'], {
                    "title": "TestGraph",
                    "nodes": [
                    {
                    "id": "v1",
                    "title": "ABC",
                    "position": {"top": 10, "left": 15, "bottom": 30, "right": 50}
                    },
                    {
                    "id": "v2",
                    "title": "DEF",
                    "position": {"top": 10, "left": 60, "bottom": 30, "right": 95}
                    },
                    {
                    "id": "v3",
                    "title": "GHI",
                    "position": {"top": 10, "left": 100, "bottom": 30, "right": 125}
                    }
                    ],
                    "edges": [
                    {"source": "v1", "target": "v2", "weight": 0.5},
                    {"source": "v1", "target": "v3", "weight": 0.8}
                    ]
                }, format='json')

        assert resp.status_code == status.HTTP_200_OK 
        assert resp.data['status'] == 'updated'

    def test_delete_graph(self):
        client = APIClient()
        self.create_graph()

        resp = client.delete(self.URLS['graph-detail-update-delete-api'])

        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert resp.data['status'] == 'deleted'

    def test_weekly_connected_node(self):
        client = APIClient()
        self.create_graph()

        resp = client.get(self.URLS['graph-weekly-connected-node-api'])

        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['Response'] == ['X2', 'X5'] 


    def tearDown(self):
        graph = Graph.objects.filter(title=self.title)
        Graph.objects.filter(title=self.title).delete()
        Node.objects.filter(graph=graph).delete()
        Edge.objects.filter(graph=graph).delete()
