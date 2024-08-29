from fastapi import *
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse , JSONResponse
from service.security import security_get_current_user , security_get_SSE_current_user
from typing import Optional
from model.model import *
from controller.notification import *
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
# from service.redis import publish_notification ,subscribe_notification
from service.redis import RedisManager
notification_router = APIRouter()

executor = ThreadPoolExecutor(max_workers=10)

@notification_router.get("/api/notification/stream" , 
                         tags=["Notification"],
                         summary = "執行 SSE 通知進 Redis",
                        description= "執行 SSE 通知進 Redis")
async def stream_notification(token: str = Query(...)):
    user = security_get_SSE_current_user(token)
    print("user:", user)
    
    
    if not user :
            error_response = ErrorResponse(error=True, message="User not authenticated")
            print("User not authenticated or authentication failed.")
            response = JSONResponse (
                    status_code=status.HTTP_403_FORBIDDEN, 
                    content=error_response.dict())
            return response
    
    redis_channel = f'notifications_channel_{user["account_id"]}'
    pubsub = RedisManager.get_redis().pubsub()
    await pubsub.subscribe(redis_channel)

    # member_id = user["account_id"]
    # pubsub = subscribe_notification(member_id)


    async def event_generator():
        try:
            count = 1
            while True :

                # print(f"start get_message: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
                # message = pubsub.get_message(timeout=5.0)
                # print(f"end get_message: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
            
                # print(f"start get_message: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
                message = await pubsub.get_message()
                # print(f"end get_message: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
            
                if message and message['type'] == 'message':
                    notification_data = json.loads(message['data'])
                    yield f"data: {json.dumps(notification_data)}\n\n"
                
                count = count + 1
                # 每 15 秒發送一次心跳
                if count >= 15:
                    a = {"type":"other"}
                    yield f"data: {json.dumps(a)}\n\n" 
                    count = 0  # 重置計數器
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Error in event_generator: {e}")
        finally:
            # Clean up: unsubscribe and close pubsub
            await pubsub.unsubscribe(redis_channel)
            await pubsub.close()
    
    # loop = asyncio.get_event_loop()
    # response = await loop.run_in_executor(executor, event_generator)

    return StreamingResponse(event_generator() , media_type="text/event-stream")


@notification_router.get("/api/notification",
        tags= ["Notification"],
        response_model = NotificationRes ,
        summary = "顯示通知：讚、回覆、追蹤",
        responses = {
            200:{
                "model" : NotificationRes,
                "description" : "成功顯示通知：讚、回覆、追蹤"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_get_notification(
    current_user :  dict = Depends(security_get_current_user),
    page: int = Query(0, description="下一頁的頁面，如果沒有更多頁為None")
    ) -> JSONResponse :
    return await get_notification(current_user , page)


@notification_router.post("/api/notification/mark_all_read",
        tags= ["Notification"],
        summary = "已讀所有最新通知",
        )
async def fetch_post_read_notification(
    request: NotificationReadRequest,
    current_user :  dict = Depends(security_get_current_user)
    ) -> JSONResponse :
    # print("request:",request)
    current_time = request.current_time
    return await post_read_notification(current_time , current_user)