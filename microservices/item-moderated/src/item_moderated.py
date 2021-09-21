import json
import redis
import requests


ITEM_MODERATED_QUEUE = "queue#item-moderated"
INDEFINITE = 0


def get_secret(path):
    with open('/etc/secrets/' + path, 'r') as secret_file:
        return secret_file.read()


try:
    # r = redis.StrictRedis(host="192.168.1.87",
    #                       port="6379",
    #                       db=0,
    #                       password="redis",
    #                       #   socket_keepalive=True,
    #                       #   socket_timeout=30,
    #                       )
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

while True:
    _, json_payload = r.blpop(ITEM_MODERATED_QUEUE, timeout=INDEFINITE)

    dict_payload = json.loads(json_payload)
    # print("JSON Payload", dict_payload["id"])
    print("JSON Payload Received", dict_payload)
    # get item  out of redis
    # json_payload = r.get(comment_key)

    # if(json_payload == None):
    #     continue

    # r.delete(comment_key)

    # Encode item as JSON
    # json_payload = json.dumps(temp)

    # Update item in Elasticsearch
    response = requests.put(
        f"http://elasticsearch-api-service/item/{dict_payload['id']}", json=dict_payload)
    # response = requests.put(f"http://localhost:9200/item/{dict_payload['id']}", json=dict_payload)
    print(response.text)

    # update author entry in redis to {"status":"finished"} with expire=28 days
    # r.set(comment_id, json_payload, ex=60*5)
    # r.rpush(POSTS_READY_QUEUE, comment_id)
