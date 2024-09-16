from fastapi import *
from fastapi import Request
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse ,RedirectResponse
import asyncio
import json
from contextlib import asynccontextmanager

##
from service.router_search import search_router
from service.router_user import user_router
from service.router_member import member_router
from service.router_post import post_router
from service.router_follow import follow_router
from service.router_comment import comment_router
from service.router_SSE import notification_router
from service.router_presigned_url import presigned_router
from service.router_bg_collection import bg_collection_router
from service.router_static import static_router 
from service.redis import RedisManager

@asynccontextmanager
async def lifespan(app: FastAPI):

    # 初始化邏輯
    await RedisManager.init_redis()

    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)
app.include_router(member_router)
app.include_router(search_router)
app.include_router(post_router)
app.include_router(follow_router)
app.include_router(comment_router)
app.include_router(notification_router)
app.include_router(presigned_router)
app.include_router(bg_collection_router)
app.include_router(static_router)

