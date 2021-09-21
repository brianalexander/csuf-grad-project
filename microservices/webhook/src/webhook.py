import json
import os
from flask import Flask
from flask import request
import redis


QUEUE_TO_PROCESS = "queue#to-process"


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

    @app.route('/webhook', methods=['POST'])
    def return_item():
        """
        Save results for moderation.

        Incoming JSON format:
        { 
            client_id: string, 
            return_url: string,
            text: string,
            priority: string [OPTIONAL]
        }
        """
        if request.method == 'POST':
            json_payload = request.get_json()
            print(json_payload)

            r.rpush(QUEUE_TO_PROCESS, json.dumps(json_payload))

            return {}, 200

    @app.route('/webhook/test', methods=['get'])
    def test_index():
        """
        test
        """
        return "working"

    return app
