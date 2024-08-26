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

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)

# manager = ConnectionManager()

# @app.websocket("/ws/notification/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, user_id: str):
#     await manager.connect(websocket)
#     pubsub = subscribe_notification(user_id)

#     try:
#         while True:
#             try:
#                 message = pubsub.get_message(timeout=5.0)
#                 if message and message['type'] == 'message':
#                     notification_data = json.loads(message['data'])
#                     await manager.send_personal_message(json.dumps(notification_data), websocket)
#             except Exception as e:
#                 print(f"Error processing message: {e}")

#             await asyncio.sleep(1)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         print(f"User {user_id} disconnected")

# ----------------------------------------------------------

# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
    return FileResponse("./static/index.html", media_type="text/html")

@app.get("/member/{account_id}", include_in_schema=False)
async def member(request: Request):
    return FileResponse("./static/member.html", media_type="text/html")

@app.get("/member/{account_id}/post/{post_id}", include_in_schema=False)
async def member_single_post(request: Request):
    return FileResponse("./static/single_page.html", media_type="text/html")

@app.get("/notification", include_in_schema=False)
async def notification(request: Request):
    return FileResponse("./static/notification.html", media_type="text/html")

@app.get("/search", include_in_schema=False)
async def search(request: Request):
    return FileResponse("./static/search.html", media_type="text/html")


@app.get("/member")
async def redirect_to_home(request: Request):
    return RedirectResponse(url="/")
 