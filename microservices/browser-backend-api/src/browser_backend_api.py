import json
import os
import time

from flask import Flask
from flask import request, make_response, jsonify
import redis


QUEUE_NEED_ITEMS = "queue#need-items"
ITEM_MODERATED_QUEUE = "queue#item-moderated"


def get_secret(path):
    with open('/etc/secrets/' + path, 'r') as secret_file:
        return secret_file.read()


try:
    r = redis.StrictRedis(host=get_secret("redis/REDIS_HOST"),
                          port=get_secret("redis/REDIS_PORT"),
                          db=get_secret("redis/REDIS_DB"),
                          password=get_secret("redis/REDIS_PASSWORD"),
                          #   socket_keepalive=True,
                          #   socket_timeout=30,
                          )

    # r = redis.StrictRedis(host="192.168.1.87",
    #                       port="6379",
    #                       db=0,
    #                       password="redis",
    #                       #   socket_keepalive=True,
    #                       #   socket_timeout=30,
    #                       )
except Exception as e:
    print("UNABLE TO CONNECT TO REDIS")
    print(e)
    exit()


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

    @app.route('/moderator/<moderator_id>/item', methods=['GET'])
    def get_items(moderator_id):
        """
        Get item batch for moderator.
        """
        moderator_id = "moderator#"+moderator_id

        if request.method == 'GET':
            print(f"getting moderator {moderator_id}")
            item = r.get(moderator_id)
            print(item)
            if (item != None):
                print("moderator is not none")
                moderator_object = json.loads(item)
            else:
                print("moderator is none")
                moderator_object = {'status': 'new'}

            # items are ready
            if (moderator_object['status'] == 'finished'):
                print("returning results...")
                r.expire(moderator_id, time=0)
                # moderator_object['status'] = 'idle'

                # r.set(moderator_id, json.dumps({'status': 'idle'}), ex=60*5)

                return jsonify({"items": moderator_object['items']}), 200

            # items are being acquired
            elif (moderator_object['status'] == 'processing' or moderator_object['status'] == 'requesting'):
                print("waiting...")
                return jsonify({"timeToWait": 1000}), 200

            # request new items
            else:
                print("requesting...")
                moderator_object['status'] = 'requesting'
                r.set(moderator_id, json.dumps(moderator_object), ex=60*5)
                r.rpush(QUEUE_NEED_ITEMS, moderator_id)

                return jsonify({"timeToWait": 1000}), 200

    @app.route('/result', methods=['POST'])
    def return_item():
        """
        Save results for moderation.

        Incoming JSON format:
        { 
            id: string,
            moderator: string, 
            tags: array[string], 
            flagged: boolean 
        }
        """
        if request.method == 'POST':
            json_payload = request.get_json()

            # epoch_time_millis = int(time.time()*1000)
            # key = f"{json_payload['id']}#{epoch_time_millis}"
            # r.set(key, json.dumps(json_payload))
            r.rpush(ITEM_MODERATED_QUEUE, json.dumps(json_payload))

            return {}, 200

    @app.route('/', methods=['get'])
    def test_index():
        """
        test
        """
        return "working"

    return app


# app = Flask(__name__)


# @app.route('/moderator/<moderator_id>/item', methods=['GET'])
# def get_items(moderator_id):
#     """
#     Get item batch for moderator.
#     """
#     if request.method == 'GET':
#         item = r.get(moderator_id)
#         if (item != None):
#             moderator_object = json.loads(item)
#         else:
#             moderator_object = {'status': 'requesting'}

#         # items are ready
#         if (moderator_object['status'] == 'finished'):
#             moderator_object['status'] = 'idle'
#             r.set(moderator_id, json.dumps(moderator_object), ex=60*5)

#             return 200, jsonify({"items": moderator_object['items']})

#         # items are being acquired
#         elif (moderator_object['status'] == 'processing' or moderator_object['status'] == 'requesting'):
#             return 200, jsonify({"timeToWait": 5000})

#         # request new items
#         else:
#             r.set(moderator_id, json.dumps(moderator_object), ex=60*5)
#             r.rpush(QUEUE_NEED_ITEMS, moderator_id)

#             return 200, jsonify({"timeToWait": 5000})


# @app.route('/result', methods=['POST'])
# def return_item(moderator_id):
#     """
#     Save results for moderation.

#     Incoming JSON format:
#     {
#         id: string,
#         moderator: string,
#         tags: array[string],
#         flagged: boolean
#     }
#     """
#     if request.method == 'POST':
#         json_payload = request.get_json()

#         epoch_time_millis = int(time.time()*1000)
#         key = f"{json_payload['id']}#{epoch_time_millis}"
#         r.set(key, json.dumps(json_payload))
#         r.rpush(ITEM_MODERATED_QUEUE, key)

#         return 200
