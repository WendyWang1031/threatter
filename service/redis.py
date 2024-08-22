import redis
import json

def publish_notification(notification_data , user_id):
    # print(f"Publishing to Redis: {notification_data}")
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    redis_channel = f'notifications_channel_{user_id}'
    
    redis_client.publish(redis_channel, json.dumps(notification_data))

def subscribe_notification(user_id):
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    pubsub = redis_client.pubsub()
    redis_channel = f'notifications_channel_{user_id}'
    pubsub.subscribe(redis_channel)
    return pubsub
   
    