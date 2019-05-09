## DjangoUnboxed

Production ready django based starter kit application.

## Technology
 - Django 1.11  LTS
 - Django Rest Framework 
 - Fully Dockerised Setup (configuration driven)
 - JWT
 - Unit tests

## Running the server locally

 * Clone this repo
 * Install python3.6
 * Intall dependencies:
> pip install -r requirements.txt
 * Run the server:
> python manage.py runserver
 * Install [docker compose](https://docs.docker.com/compose/install/)
 * Run docker:
> docker-compose build

> docker-compose up
 * To check the server, open `http://localhost:8001/`


## License

This project is licensed under the terms of the MIT license.


1. docker-compose build

2. docker-compose up


Header: application / json is common for all api's

1. Api to get all graph from the system:
GET : http://localhost:8001/api/v1.0/boilerplate_apps/graph
Response:
   {
       "Response": [
           {
               "title": "Graph123",
               "nodes": [
                   {
                       "id": "v1",
                       "title": "ABC",
                       "position": {
                           "top": 10,
                           "left": 15,
                           "right": 50,
                           "bottom": 30
                       }
                   },
                   {
                       "id": "v2",
                       "title": "DEF",
                       "position": {
                           "top": 10,
                           "left": 60,
                           "right": 95,
                           "bottom": 30
                       }
                   },
                   {
                       "id": "v3",
                       "title": "GHI",
                       "position": {
                           "top": 10,
                           "left": 100,
                           "right": 125,
                           "bottom": 30
                       }
                   }
               ],
               "edges": [
                   {
                       "source": "v1",
                       "target": "v2",
                       "weight": 0.5
                   },
                   {
                       "source": "v1",
                       "target": "v3",
                       "weight": 0.8
                   }
               ]
           }
       ]
   }


2. Api to create graph:
POST : http://localhost:8001/api/v1.0/boilerplate_apps/graph/
Data : {
      "title": "Graph123",
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
   }
Response:
   {
       "status": "Graph created successfully"
   }


3. Get a single graph:
GET: http://localhost:8001/api/v1.0/boilerplate_apps/graph/Graph123/
Response:
 {
    "Response": {
        "title": "Graph123",
        "nodes": [
            {
                "id": "v1",
                "title": "ABC",
                "position": {
                    "top": 10,
                    "left": 15,
                    "right": 50,
                    "bottom": 30
                }
            },
            {
                "id": "v2",
                "title": "DEF",
                "position": {
                    "top": 10,
                    "left": 60,
                    "right": 95,
                    "bottom": 30
                }
            },
            {
                "id": "v3",
                "title": "GHI",
                "position": {
                    "top": 10,
                    "left": 100,
                    "right": 125,
                    "bottom": 30
                }
            }
        ],
        "edges": [
            {
                "source": "v1",
                "target": "v2",
                "weight": 0.5
            },
            {
                "source": "v1",
                "target": "v3",
                "weight": 0.8
            }
        ]
    }
}

4. Update a graph:
PUT : http://localhost:8001/api/v1.0/boilerplate_apps/graph/<graph_title>/
Example: http://localhost:8001/api/v1.0/boilerplate_apps/graph/Graph123/
Body params : 
   {
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
   }
Response:
   {
       "status": "Graph is updated successfully"
   }


5. Delete a single graph
DEL : http://localhost:8001/api/v1.0/boilerplate_apps/graph/Graph123/
Response: 
   {
    "status": "Graph is deleted successfully"
   }


6. CSV file to add nodes
POST : http://localhost:8001/api/v1.0/boilerplate_apps/parse_node_csv/Graph123/
Data: {'nodes_csv': <csv_file>}
- CSV Format should be like:
   x1,XYZ,10,15,30,35
   x2,SGDG,15,10,50,40
   x3,DGS,20,40,35,25

Response: 
   {
       "Response": "Nodes updated from csv successfully"
   }

7. Get "weakly connected" nodes for the graph:
GET: http://localhost:8001/api/v1.0/boilerplate_apps/weakly_connected_nodes/Graph123/
Response : 
{
    "weakly_bound_nodes": [
        {
            "id": 41,
            "nod_id": "v2",
            "title": "DEF",
            "position": {
                "top": 10,
                "left": 60,
                "right": 95,
                "bottom": 30
            }
        }
    ]
}

8. Get disjoint graph and rectangle:
GET : http://localhost:8001/api/v1.0/boilerplate_apps/islands/Graph123/
Response:
{
    "Disjoint islands": [
        [
            "x1"
        ],
        [
            "x2"
        ],
        [
            "x3"
        ],
        [
            "x4"
        ],
        [
            "x5"
        ]
    ],
    "bounding_rectangle_coordinates": {
        "point1": {
            "top": 9,
            "left": 9,
            "bottom": 51,
            "right": 126
        },
        "point2": {
            "top": 9,
            "left": 101,
            "bottom": 51,
            "right": 24
        },
        "point3": {
            "top": 51,
            "left": 9,
            "bottom": 29,
            "right": 126
        },
        "point4": {
            "top": 51,
            "left": 101,
            "bottom": 29,
            "right": 24
        }
    }
}

9. Api to get overlap node:
GET: http://localhost:8001/api/v1.0/boilerplate_apps/get_overlap_node/Graph123/
body : {"top":5, "left": 5, "bottom": 20, "right": 20}
Response : {
    "full_nodes": [
        {
            "id": 35,
            "nod_id": "v2",
            "title": "DEF",
            "position": {
                "top": 10,
                "left": 60,
                "right": 95,
                "bottom": 30
            }
        },
        {
            "id": 36,
            "nod_id": "v3",
            "title": "GHI",
            "position": {
                "top": 10,
                "left": 100,
                "right": 125,
                "bottom": 30
            }
        }
    ]
}
Response:
   {
       "full_nodes": [
           {
               "id": 41,
               "nod_id": "v2",
               "title": "DEF",
               "position": {
                   "top": 10,
                   "left": 60,
                   "right": 95,
                   "bottom": 30
               }
           },
           {
               "id": 42,
               "nod_id": "v3",
               "title": "GHI",
               "position": {
                   "top": 10,
                   "left": 100,
                   "right": 125,
                   "bottom": 30
               }
           }
       ]
   }

10. Shell script to convert the CSV format expected by the API.
Command: python import_data.py <graph_title> <comma seaprated file names>
Example: python import_data.py graph11 node1.csv,node2.csv



