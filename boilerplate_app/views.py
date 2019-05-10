# python imports
import io
import csv
import requests

# Django imports
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError  

# Rest Framework imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

#Third Party Imports
import networkx as nx

# local imports
from rest_framework.renderers import JSONRenderer
from boilerplate_app.models import Graph, Node, Edge
from boilerplate_app.serializers import GraphSerializer, NodeSerializer
from django.db.models.functions import Cast
from django.db.models import Min, Max, IntegerField
from django.contrib.postgres.fields.jsonb import KeyTextTransform
import json


class GraphListCreateAPIView(APIView):
    serializer_class = GraphSerializer

    def get(self, request, format=None):
        """
        List all the graphs. But we can add pagination here
        """
        graph = Graph.objects.all()
        graph_serializer = GraphSerializer(graph, many=True)
        graphs = graph_serializer.data
        return Response({'Response': graphs},
                        status=status.HTTP_200_OK)
        
    def post(self, request, format=None):
        """
        Create nodes, edges and graph
        """
        try:
            graph = Graph.objects.get(title=request.data.get('title'))
            return Response({'detail': 'Graph with this title already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            graph = Graph.objects.create(title=request.data.get('title'))
            for node in request.data.get('nodes'):
                try:
                    Node.objects.get(nod_id=node['id'], graph=graph)
                except ObjectDoesNotExist:
                    Node.objects.create(nod_id=node['id'], title=node['title'], position=node['position'], graph=graph)
            for edge in request.data.get('edges'):
                try:
                    Edge.objects.get(source=Node.objects.get(nod_id=edge['source'], graph=graph), target=Node.objects.get(nod_id=edge['target'], graph=graph), graph=graph)
                except:
                    Edge.objects.create(source=Node.objects.get(nod_id=edge['source'], graph=graph), target=Node.objects.get(nod_id=edge['target'], graph=graph), weight=edge['weight'], graph=graph)
            return Response({'status': 'Graph created successfully'}, status=status.HTTP_201_CREATED)



class GraphDetailUpdateDeleteAPIView(APIView):

    def get(self, request, title, format=None):
        """
        List the details of a graph
        """
        try:
            graph = Graph.objects.get(title=title)
        except ObjectDoesNotExist:
            return Response({'Response': 'Invalid Graph Title'},
                        status=status.HTTP_204_NO_CONTENT)
        graph_serializer = GraphSerializer(graph)

        graphs = graph_serializer.data
        return Response({'Response': graphs},
                        status=status.HTTP_200_OK)

    def put(self, request, title, format=None):
        """
        Update a graph
        """
        try:
            graph = Graph.objects.get(title=title)
        except ObjectDoesNotExist:
            return Response({'Response': 'Invalid Graph Title'},
                        status=status.HTTP_204_NO_CONTENT)

        nodes = Node.objects.filter(graph=graph).delete()
        edges = Edge.objects.filter(graph=graph).delete()


        for node in request.data.get('nodes'):
            Node.objects.create(nod_id=node['id'], title=node['title'], position=node['position'], graph=graph)
        for edge in request.data.get('edges'):
            Edge.objects.create(source=Node.objects.get(nod_id=edge['source'], graph=graph), target=Node.objects.get(nod_id=edge['target'], graph=graph), weight=edge['weight'], graph=graph)
        return Response({'status': 'Graph is updated successfully'},
                        status=status.HTTP_200_OK)


    def delete(self, request, title, format=None):
        """
        Delete a graph
        """
        try:
            Graph.objects.get(title=title).delete()
        except ObjectDoesNotExist:
            return Response({'Response': 'Invalid Graph Title'},
                        status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'Graph is deleted successfully'},
                        status=status.HTTP_200_OK)


class GraphWeaklyConnectedNodeAPIView(APIView):

    def get(self, request, title, format=None):
        """
        Find the weekly connected nodes of a graph
        """
        try:
            graph = Graph.objects.get(title=title)
        except ObjectDoesNotExist:
            return Response({'Response': 'Invalid Graph Title'},
                        status=status.HTTP_204_NO_CONTENT)
        edges = Edge.objects.filter(graph=graph)
        # node_list = Node.objects.filter(graph=graph).values_list('nod_id', flat=True)
        # node_list = [node for node in node_list]
        connected_nodes = []

        weakly_bound_nodes = []
        strongly_bound_nodes = []
        
        for edge in edges:
            # connected_nodes.extend([edge.source.nod_id, edge.target.nod_id])
            if edge.weight <= 0.5 and edge.target.nod_id not in strongly_bound_nodes:
                weakly_bound_nodes.append(edge.target.nod_id)
            elif edge.weight > 0.5 and edge.target.nod_id in weakly_bound_nodes:
                weakly_bound_nodes.remove(edge.target.nod_id) 
                strongly_bound_nodes.append(edge.target.nod_id)
            else:
                strongly_bound_nodes.append(edge.target.nod_id)

        # connected_nodes = list(set(connected_nodes))
        # weakly_bound_nodes.append([node for node in node_list if node not in connected_nodes])
        nodes = Node.objects.filter(graph=graph, nod_id__in=weakly_bound_nodes)
        node_serializer = NodeSerializer(nodes, many=True)
        return Response({ 'weakly_bound_nodes': node_serializer.data },
                        status=status.HTTP_200_OK)


class ParseNodeCSVAPIView(APIView):

    def post(self, request, title, format=None):
        """
        parse node data as CSV and add the resulting nodes to an existing graph
        """
        try:
            graph = Graph.objects.get(title=title)
        except ObjectDoesNotExist:
            return Response({'Response': 'Invalid Graph Title'},
                        status=status.HTTP_204_NO_CONTENT)
        csv_file = request.data['nodes_csv']
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        for row in csv.reader(io_string, delimiter=','):
            try:
                Node.objects.get(nod_id=row[1], graph=graph)
            except ObjectDoesNotExist:
                Node.objects.create(nod_id=row[0], title=row[1], position={'top': row[2], 'left': row[3], 'bottom': row[4], 'right': row[5]}, graph=graph)
        return Response({'Response': 'Nodes updated from csv successfully'},
                        status=status.HTTP_200_OK)


class GraphListIslandsAPIView(APIView):

    def get(self, request, title, format=None):
        """
        Returns islands in a graph
        """
        try:
            graph=Graph.objects.get(title=title)
        except ObjectDoesNotExist:
            return Response({'Response': 'Invalid Graph Title'},
                        status=status.HTTP_204_NO_CONTENT)

        node_list = Node.objects.filter(graph=graph).values_list('nod_id', flat=True)
        edge_list = Edge.objects.filter(graph=graph).values_list('source__nod_id', 'target__nod_id')

        graph_obj = nx.Graph(title=title)
        graph_obj.add_nodes_from(node_list)
        graph_obj.add_edges_from(edge_list)

        islands = list(nx.connected_component_subgraphs(graph_obj, copy=True))
        island_list = [list(island.nodes) for island in islands]

        bounding_rectangle_coordinates = []
        for island in island_list:
            if len(island) == 1:
                node = Node.objects.get(graph=graph, nod_id__in=island)
                min_top = max_top = int(node.position['top'])
                min_left = max_left = int(node.position['left'])
                min_bottom = max_bottom = int(node.position['bottom'])
                min_right = max_right = int(node.position['right'])
            else:
                min_top = Node.objects.filter(graph=graph, nod_id__in=island).annotate(top=Cast(KeyTextTransform('top', 'position'), IntegerField())).aggregate(Min('top')).get('top__min')
                max_top = Node.objects.filter(graph=graph, nod_id__in=island).annotate(top=Cast(KeyTextTransform('top', 'position'), IntegerField())).aggregate(Max('top')).get('top__max')

                min_left = Node.objects.filter(graph=graph, nod_id__in=island).annotate(left=Cast(KeyTextTransform('left', 'position'), IntegerField())).aggregate(Min('left')).get('left__min')
                max_left = Node.objects.filter(graph=graph, nod_id__in=island).annotate(left=Cast(KeyTextTransform('left', 'position'), IntegerField())).aggregate(Max('left')).get('left__max')

                min_bottom = Node.objects.filter(graph=graph, nod_id__in=island).annotate(bottom = Cast(KeyTextTransform('bottom', 'position'), IntegerField())).aggregate(Min('bottom')).get('bottom__min')
                max_bottom = Node.objects.filter(graph=graph, nod_id__in=island).annotate(bottom=Cast(KeyTextTransform('bottom', 'position'), IntegerField())).aggregate(Max('bottom')).get('bottom__max')

                min_right = Node.objects.filter(graph=graph, nod_id__in=island).annotate(right=Cast(KeyTextTransform('right', 'position'), IntegerField())).aggregate(Min('right')).get('right__min')
                max_right = Node.objects.filter(graph=graph, nod_id__in=island).annotate(right=Cast(KeyTextTransform('right', 'position'), IntegerField())).aggregate(Max('right')).get('right__max')

            bounding_rectangle_coordinates.append(
                {
                    'island': ",".join(island),
                    'bounding_rectangle_points': {
                        'point1': {"top": min_top - 1, "left": min_left - 1, "bottom": max_bottom + 1, "right": max_right + 1},
                        'point2': {"top": min_top - 1, "left": max_left + 1, "bottom": max_bottom + 1, "right": min_right -1},
                        'point3': {"top": max_top + 1, "left": min_left - 1, "bottom": min_bottom-1, "right": max_right+1},
                        'point4': {"top": max_top + 1, "left": max_left + 1, "bottom": min_bottom - 1, "right": min_right - 1}
                    }
            }

        )
        # min_top = Node.objects.filter(graph=graph).annotate(top=Cast(KeyTextTransform('top', 'position'), IntegerField())).aggregate(Min('top')).get('top__min')
        # max_top = Node.objects.filter(graph=graph).annotate(top=Cast(KeyTextTransform('top', 'position'), IntegerField())).aggregate(Max('top')).get('top__max')

        # min_left = Node.objects.filter(graph=graph).annotate(left=Cast(KeyTextTransform('left', 'position'), IntegerField())).aggregate(Min('left')).get('left__min')
        # max_left = Node.objects.filter(graph=graph).annotate(left=Cast(KeyTextTransform('left', 'position'), IntegerField())).aggregate(Max('left')).get('left__max')

        # min_bottom = Node.objects.filter(graph=graph).annotate(bottom = Cast(KeyTextTransform('bottom', 'position'), IntegerField())).aggregate(Min('bottom')).get('bottom__min')
        # max_bottom = Node.objects.filter(graph=graph).annotate(bottom=Cast(KeyTextTransform('bottom', 'position'), IntegerField())).aggregate(Max('bottom')).get('bottom__max')

        # min_right = Node.objects.filter(graph=graph).annotate(right=Cast(KeyTextTransform('right', 'position'), IntegerField())).aggregate(Min('right')).get('right__min')
        # max_right = Node.objects.filter(graph=graph).annotate(right=Cast(KeyTextTransform('right', 'position'), IntegerField())).aggregate(Max('right')).get('right__max')

        # bounding_rectangle_coordinates = {
        #     'point1': {"top": min_top - 1, "left": min_left - 1, "bottom": max_bottom + 1, "right": max_right + 1},
        #     'point2': {"top": min_top - 1, "left": max_left + 1, "bottom": max_bottom + 1, "right": min_right -1},
        #     'point3': {"top": max_top + 1, "left": min_left - 1, "bottom": min_bottom-1, "right": max_right+1},
        #     'point4': {"top": max_top + 1, "left": max_left + 1, "bottom": min_bottom - 1, "right": min_right - 1}
        #     }        
        return Response({ 'Disjoint islands': island_list, 'bounding_rectangle_coordinates': bounding_rectangle_coordinates },
                        status=status.HTTP_200_OK)         

class GetOverlapNodesAPIView(APIView):
    serializer_class = NodeSerializer

    def get(self, request, title, format=None):
        """
        Get full overlaps nodes
        """
        try:
            graph = Graph.objects.get(title=title)
            if request.body:
                rectangle_data = json.loads(request.body)
                node_ids = Node.objects.filter(graph=graph).filter(position__top__gt = rectangle_data['top']).filter(position__left__gt = rectangle_data['left']).filter(position__top__lt = rectangle_data['bottom']).filter(position__left__lt = rectangle_data['right']).values_list('id', flat=True)
                returning_node_ids = Edge.objects.filter(source_id__in = node_ids).values_list('target_id', flat=True) 
                returning_nodes = Node.objects.filter(id__in  =returning_node_ids)
                node_serializer = NodeSerializer(returning_nodes, many=True)
                return Response({'full_nodes': node_serializer.data }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'Graph with this title is not found'}, status=status.HTTP_400_BAD_REQUEST)