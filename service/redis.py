import redis
import json
import datetime
from model.model import *
import os


REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def publish_notification(notification_data: NotifyInfo, member_id: str):
    
    redis_channel = f'notifications_channel_{member_id}'
    notification_dict = notification_data.dict()
    redis_client.publish(redis_channel, json.dumps(notification_dict))

def subscribe_notification(user_id):
    pubsub = redis_client.pubsub()
    redis_channel = f'notifications_channel_{user_id}'
    pubsub.subscribe(redis_channel)
    return pubsub
   
    