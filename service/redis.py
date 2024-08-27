import redis.asyncio as redis
import json
import datetime
from model.model import *
import os


REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

'''
def publish_notification(notification_data: NotifyInfo, member_id: str):
    
    redis_channel = f'notifications_channel_{member_id}'
    notification_dict = notification_data.dict()
    redis_client.publish(redis_channel, json.dumps(notification_dict))

def subscribe_notification(user_id):
    pubsub = redis_client.pubsub()
    redis_channel = f'notifications_channel_{user_id}'
    pubsub.subscribe(redis_channel)
    return pubsub
'''


class RedisManager:
    _redis_instance = None

    @classmethod
    async def init_redis(cls) -> None:
        try:
            if cls._redis_instance is None:
                cls._redis_instance = await redis.from_url(
                    f"redis://{REDIS_HOST}:{REDIS_PORT}",
                    db=0
                )
            await cls._redis_instance.ping()
        except Exception as e:
            raise RuntimeError(f"Init Redis Fail, Error: {e}")

    @classmethod
    def get_redis(cls) -> redis.Redis:
        if cls._redis_instance is None:
            raise RuntimeError("Redis instance is not initialized")
        return cls._redis_instance
    
    @classmethod
    async def cache_popular_posts(cls,  page: int, posts: List[dict], expiration: int = 600) -> None:
        redis_key = f"popular_posts:page_{page}"
        
        if cls._redis_instance is None:
            raise RuntimeError("Redis instance is not initialized")
        
        async with cls._redis_instance.pipeline() as pipe:
            for post in posts['data']:
                post_id = post["post_id"]
                post_data = json.dumps(post)
                pipe.hset(redis_key, post_id, post_data)
            pipe.expire(redis_key, expiration)  
            await pipe.execute()

    @classmethod
    async def get_popular_posts(cls, page: int) -> List[dict]:
        redis_key = f"popular_posts:page_{page}"
        
        if cls._redis_instance is None:
            raise RuntimeError("Redis instance is not initialized")
        
        posts = await cls._redis_instance.hgetall(redis_key)
        post_list = []
        if posts:
            for post_id, post_data in posts.items():
                post_id = post_id.decode('utf-8')
                post_data = post_data.decode('utf-8')

                post_dict = json.loads(post_data)
                post_dict["post_id"] = post_id
                post_list.append(post_dict)

        return post_list

    
    @classmethod
    async def publish_notification(cls, notification_data: NotifyInfo, member_id: str) -> None:
        if cls._redis_instance is None:
            raise RuntimeError("Redis instance is not initialized")
        
        redis_channel = f'notifications_channel_{member_id}'
        notification_dict = notification_data.dict()
        await cls._redis_instance.publish(redis_channel, json.dumps(notification_dict))

    @classmethod
    async def close_redis(cls) -> None:
        if cls._redis_instance is not None:
            await cls._redis_instance.close()
            cls._redis_instance = None
