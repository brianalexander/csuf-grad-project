import json
import redis
import requests
import random


INTAKE_PROCESSED_QUEUE = "queue#intake-processed"
INDEFINITE = 0


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
    #                 port="6379",
    #                 db=0,
    #                 password="redis",
    #                 #   socket_keepalive=True,
    #                 #   socket_timeout=30,
    #                 )
except Exception as e:
    print("UNABLE TO CONNECT TO REDIS")
    print(e)
    exit()

bins = ["low", "medium", "high"]
print("waiting for items...")
while True:
    _, item_json = r.blpop(INTAKE_PROCESSED_QUEUE, timeout=INDEFINITE)

    # get item  out of redis
    # temp = r.get(item)
    if(item_json == None):
        continue

    # print("item", item_json)

    item = json.loads(item_json)

    # TODO: Uncomment initializations
    item['finished'] = False
    item['flagged'] = False

    # TODO: REMOVE DUMMY DATA
    # item['finished'] = True if random.randint(0, 1) == 1 else False
    # item['flagged'] = True if random.randint(0, 1) == 1 else False

    item['moderatedCount'] = 0
    item['flaggedCount'] = 0

    item['moderatedBy'] = []
    item['embedding'] = item['embedding']

    # TODO: REMOVE DUMMY DATA
    # item['bin'] = bins[random.randint(0, 2)]

    # TODO: SET BIN FROM WEBHOOK REQUEST
    if (item['priority'] == 'high'):
        item['bin'] = 'high'
    elif (item['priority'] == 'medium'):
        item['bin'] = 'medium'
    else:
        item['bin'] = 'low'

    del item['priority']

    # TODO: REMOVE DUMMY DATA
    # item['tags'] = ["".join(["tag", str(num)])
    #                 for num in range(random.randint(1, 5))]

    # TODO: re-enable and TEST THIS
    # [
    #     {"text": "Hate Speech", "value": random.uniform(0, 1)},
    #     {"text": "Toxicity", "value": random.uniform(0, 1)},
    #     {"text": "Offensiveness", "value": random.uniform(0, 1)},
    # ]
    item['tags'] = []
    print("SCORES ", item['scores'])
    for score in item['scores']:
        if(float(score['value']) > 0.25):
            item['tags'].append(score['text'])

    # # TODO: REMOVE DUMMY DATA
    # item['similarItems'] = [
    #     {
    #         "text": "this is a 1",
    #         "tags": ["".join(["tag", str(num)])
    #                  for num in range(random.randint(1, 5))],
    #         "flagged": bool(random.randint(0, 1))
    #     },
    #     {
    #         "text": "this is a 2",
    #         "tags": ["".join(["tag", str(num)])
    #                  for num in range(random.randint(1, 5))],
    #         "flagged": bool(random.randint(0, 1))
    #     },
    #     {
    #         "text": "this is a 3",
    #         "tags": ["".join(["tag", str(num)])
    #                  for num in range(random.randint(1, 5))],
    #         "flagged": bool(random.randint(0, 1))
    #     },
    #     {
    #         "text": "this is a 4",
    #         "tags": ["".join(["tag", str(num)])
    #                  for num in range(random.randint(1, 5))],
    #         "flagged": bool(random.randint(0, 1))
    #     },
    # ]
    # TODO: GET ACTAUL SIMILAR ITEMS
    response = requests.get(
        f"http://elasticsearch-api-service/item?similarTo={item['embedding']}")
    response_json = response.json()

    print("RESPONSE", response_json['hits']['hits'])

    item['similarItems'] = []
    for resp in response_json['hits']['hits']:
        similar_item = {
            "text": resp['_source']['text'],
            "tags": resp['_source']['tags'],
            "flagged": resp['_source']['flagged']
        }
        print("SIMILAR_ITEM", similar_item)
        item['similarItems'].append(similar_item)

    # Add item to Elasticsearch
    response = requests.post(
        "http://elasticsearch-api-service/item", json=item)
    # response = requests.post("http://192.168.1.87:8080/item", json=item)

    # print(response.text)
