from fastapi import FastAPI, APIRouter, BackgroundTasks
from service.redis import RedisManager
from controller.cache_public_post import get_popular_to_zset_posts

bg_collection_router = APIRouter()

@bg_collection_router.post("/collect_popular_posts")
async def trigger_collection(background_tasks: BackgroundTasks):
    background_tasks.add_task(get_popular_to_zset_posts, 30)
    return {"message": "Popular post collection started in the background."}