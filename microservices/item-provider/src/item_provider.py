import json

import redis
import requests

QUEUE_NEED_ITEMS = "queue#need-items"
INDEFINITE = 0
ELASTICSEARCH_API_ADDRESS = "http://elasticsearch-api-service"
# ELASTICSEARCH_API_ADDRESS = "http://localhost:8080"


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


while True:
    _, moderator_key = r.blpop(QUEUE_NEED_ITEMS, timeout=INDEFINITE)
    print(moderator_key)
    moderator_object = json.loads(r.get(moderator_key))
    _, moderator_id = str(moderator_key, 'utf-8').split("#")
    print(moderator_id)
    if(moderator_object['status'] == "requesting"):
        moderator_object['status'] = "processing"
        r.set(moderator_key, json.dumps(moderator_object), ex=60*5)

        print(f"requesting items for {moderator_id}...")

        response = requests.get(
            f"{ELASTICSEARCH_API_ADDRESS}/item?moderator={moderator_id}")

        print(response.text)

        # finished TODO: Set user to {'status': 'processing'}
        # TODO: Get 10 new items for user from elasticsearch api
        response_json = response.json()
        moderator_object['items'] = response_json['hits']['hits']

        # TODO: Set current user on Redis with items and set status to 'finished'
        moderator_object['status'] = "finished"
        r.set(moderator_key, json.dumps(moderator_object), ex=60*5)
