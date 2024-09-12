from service.redis import RedisManager
from db.cache_public_post import *

async def get_popular_to_zset_posts(time_frame: int):

    await RedisManager.init_redis()
    redis_client = RedisManager.get_redis()

    post_ids = db_get_popular_to_zset_posts(time_frame)
    if post_ids is None:
        print("Failed to retrieve post IDs")
        return

    # 更新 ZSET 排名，增加每篇貼文的分數
    for post_id in post_ids:
        await redis_client.zincrby("popular_posts_zset", 1, post_id) 

    print(f"Updated ZSET with post IDs from time frame {time_frame}")

