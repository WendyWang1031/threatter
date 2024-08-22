import redis
import json

def publish_notification_to_redis(notification_data):
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    redis_channel = 'notifications_channel'
    
    redis_client.publish(redis_channel, json.dumps(notification_data))
    
def subscribe_to_notifications():
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    pubsub = redis_client.pubsub()
    pubsub.subscribe('notifications_channel')
    return pubsub