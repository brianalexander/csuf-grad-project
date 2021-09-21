import json
import os

from flask import Flask
from flask import request
import requests

INDEX_ADDRESS = "http://elasticsearch/item"
# INDEX_ADDRESS = "http://192.168.1.87:9200/item"


def get_secret(path):
    with open('/etc/secrets/' + path, 'r') as secret_file:
        return secret_file.read()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/item', methods=['GET'])
    def search_item():
        """
        Return set of items based on query paremeters.

        similarTo: Accepts vector.
            Ex. similarTo=[1,2,3]
        moderator: Accepts string.
            Ex. moderator=Bob
        """
        if request.method == 'GET':
            if('similarTo' in request.args):
                json_payload = {
                    "from": 0, "size": 4,
                    "query": {
                        "script_score": {
                            "query": {
                                "bool": {
                                    "must": {
                                        "term": {
                                            "finished": True
                                        }
                                    }
                                }
                            },
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                                "params": {"query_vector": json.loads(request.args['similarTo'])}
                            }
                        }
                    }
                }

                r = requests.post(INDEX_ADDRESS+"/_search",
                                  json=json_payload)

                return r.json(), r.status_code

            if('moderator' in request.args):
                json_payload = {
                    "from": 0, "size": 10,
                    "query": {
                        "bool": {
                            "must_not": [
                                {
                                    "term": {
                                        "moderatedBy": request.args['moderator'],
                                    }
                                },
                                {
                                    "term": {
                                        "finished": True
                                    }
                                }
                            ]
                        }
                    }
                }

                r = requests.post(INDEX_ADDRESS+"/_search",
                                  json=json_payload)

                return r.json(), r.status_code

            return {}, 500

    @app.route('/item', methods=['POST'])
    def create_item():
        """
        Called by Intake Processed Service.
        """
        if request.method == 'POST':
            json_payload = request.get_json()
            print("saving...", json_payload)

            r = requests.post(INDEX_ADDRESS+"/_doc", json=json_payload)
            return r.json(), r.status_code

    @app.route('/item/<id>', methods=['PUT'])
    def update_item(id):
        """
        Called by Item Moderated Service.
        """
        if request.method == 'PUT':
            request_json = request.get_json()
            json_payload = {
                "script": {
                    "source": "if(ctx._source.finished){ return; } for (moderator in ctx._source.moderatedBy) { if(moderator == params.moderator){ return; } } for (item in params.tags) { ctx._source.tags.add(item); } if (params.flagged) { ctx._source.flaggedCount++; } ctx._source.moderatedCount++; ctx._source.moderatedBy.add(params.moderator); if (ctx._source.flaggedCount / 2 > 0.5) { ctx._source.flagged = true; } if (ctx._source.moderatedCount >= 3) { ctx._source.finished = true; }",
                    "lang": "painless",
                    "params": {
                        "tags": request_json["tags"],
                        "moderator": request_json["moderator"],
                        "flagged": request_json["flagged"]
                    }
                }
            }

            r = requests.post(INDEX_ADDRESS+"/_update"+"/" + id,
                              json=json_payload)
            return r.json(), r.status_code

    return app

# app = Flask(__name__)


# @app.route('/item', methods=['GET'])
# def search_item():
#     """
#     Called by Task Provider Service.
#     """
#     if request.method == 'GET':
#         if('similarTo' in request.args):
#             json_payload = {
#                 "from": 0, "size": 10,
#                 "query": {
#                     "script_score": {
#                         "query": {"match_all": {}},
#                         "script": {
#                             "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
#                             "params": {"query_vector": json.loads(request.args['similarTo'])}
#                         }
#                     }
#                 }
#             }

#             r = requests.post(INDEX_ADDRESS+"/_search",
#                               json=json_payload)

#             return r.json(), r.status_code
#         return {}, 500


# @app.route('/item', methods=['POST'])
# def create_item():
#     """
#     Called by Intake Processed Service.
#     """
#     if request.method == 'POST':
#         json_payload = request.get_json()
#         r = requests.post(INDEX_ADDRESS+"/_doc", json=json_payload)
#         return r.json(), r.status_code


# @app.route('/item/<id>', methods=['PUT'])
# def update_item(id):
#     """
#     Called by Item Moderated Service.
#     """
#     if request.method == 'PUT':
#         request_json = request.get_json()
#         json_payload = {
#             "script": {
#                 "source": "if(ctx._source.finished){ return; } for (item in params.tags) { ctx._source.tags.add(item); } if (params.flagged) { ctx._source.flaggedCount++; } ctx._source.moderatedCount++; ctx._source.moderatedBy.add(params.moderator); if (ctx._source.flaggedCount / 2 > 0.5) { ctx._source.flagged = true; } if (ctx._source.moderatedCount >= 3) { ctx._source.finished = true; }",
#                 "lang": "painless",
#                 "params": {
#                     "tags": request_json["tags"],
#                     "moderator": request_json["moderator"],
#                     "flagged": request_json["flagged"]
#                 }
#             }
#         }

#         r = requests.post(INDEX_ADDRESS+"/_update"+"/"+id,
#                           json=json_payload)
#         return r.json(), r.status_code
