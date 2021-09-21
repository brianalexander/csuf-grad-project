import json
import random

import numpy as np
import redis

# S-BERT
from sentence_transformers import SentenceTransformer

# HuggingFace
from transformers import BertForSequenceClassification, BertTokenizerFast, BertConfig

# PyTorch
import torch

QUEUE_TO_PROCESS = "queue#to-process"
QUEUE_INTAKE_PROCESSED = "queue#intake-processed"
INDEFINITE = 0

MAX_LENGTH = 500
BATCH_SIZE = 1
DEVICE = 'cpu'


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


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

# initialize BERT for Toxicity
config = BertConfig.from_pretrained('bert-base-uncased')
config.num_labels = 1

toxic_model = BertForSequenceClassification(config)
offensive_model = BertForSequenceClassification(config)
hatespeech_model = BertForSequenceClassification(config)

toxic_model.load_state_dict(torch.load(
    "/models/toxic/toxic_sd.pt"))
offensive_model.load_state_dict(torch.load(
    "/models/offensive/offensive_sd.pt"))
hatespeech_model.load_state_dict(torch.load(
    "/models/hatespeech/hatespeech_sd.pt"))

toxic_model.to('cpu')
offensive_model.to('cpu')
hatespeech_model.to('cpu')
# for param in toxic_model.parameters():
#     param.requires_grad = False
toxic_model.eval()
offensive_model.eval()
hatespeech_model.eval()
print("models ready for evaluation...")

tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")

# initialize S-BERT
sbert_model = SentenceTransformer('paraphrase-distilroberta-base-v1')
sbert_model.max_seq_length = MAX_LENGTH

# get item from queue
while True:
    _, item_json = r.blpop(QUEUE_TO_PROCESS, timeout=INDEFINITE)
    # temp = r.get(comment_id)
    # print(f"got {comment_id}")
    if(item_json == None):
        continue
    print(item_json)
    item = json.loads(item_json)

    # Get comment similarity embedding
    item['embedding'] = sbert_model.encode([item['text']])[0]

    # Prepare Model Input
    model_input = tokenizer(
        item['text'], truncation=True, padding="max_length", max_length=MAX_LENGTH)
    input_ids = torch.tensor(model_input['input_ids'], dtype=torch.long).to(
        DEVICE).view(BATCH_SIZE, MAX_LENGTH)
    attention_mask = torch.tensor(model_input['attention_mask'], dtype=torch.long).to(
        DEVICE).view(BATCH_SIZE, MAX_LENGTH)

    # Classify inputs
    pred = toxic_model(input_ids=input_ids, attention_mask=attention_mask)
    toxic_score = torch.sigmoid(pred['logits'].detach().cpu().squeeze())

    pred = offensive_model(input_ids=input_ids, attention_mask=attention_mask)
    offensive_score = torch.sigmoid(pred['logits'].detach().cpu().squeeze())

    pred = hatespeech_model(input_ids=input_ids, attention_mask=attention_mask)
    hatespeech_score = torch.sigmoid(pred['logits'].detach().cpu().squeeze())

    # add scores to data
    item['scores'] = [
        {"text": "Hate Speech", "value": float(hatespeech_score)},
        {"text": "Toxic", "value": float(toxic_score)},
        {"text": "Offensive", "value": float(offensive_score)},
    ]

    # add item to queue
    r.rpush(QUEUE_INTAKE_PROCESSED, json.dumps(item, cls=NumpyEncoder))
