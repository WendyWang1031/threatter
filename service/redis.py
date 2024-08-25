import redis
import json
import datetime
from model.model import *
import os

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

def publish_notification(notification_data: NotifyInfo, member_id: str):
    # print(f"Publishing to Redis: {notification_data}")
    redis_client = redis.Redis(host=REDIS_PORT, port=6379, db=0)
    redis_channel = f'notifications_channel_{member_id}'
    notification_dict = notification_data.dict()
    
    redis_client.publish(redis_channel, json.dumps(notification_dict))

def subscribe_notification(user_id):
    redis_client = redis.Redis(host=REDIS_PORT, port=6379, db=0)
    pubsub = redis_client.pubsub()
    redis_channel = f'notifications_channel_{user_id}'
    pubsub.subscribe(redis_channel)
    return pubsub
   
    