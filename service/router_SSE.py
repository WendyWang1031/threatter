from fastapi import *
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse , JSONResponse
from service.security import security_get_current_user , security_get_SSE_current_user
from typing import Optional
from model.model import *
from controller.notification import *
import asyncio

notification_router = APIRouter()

@notification_router.get("/api/notification/stream" , tags=["Notification"])
async def stream_notification(token: str = Query(...),
                              ):
    user = security_get_SSE_current_user(token)
    # print("user:", user)
    
    if not user :
            error_response = ErrorResponse(error=True, message="User not authenticated")
            print("User not authenticated or authentication failed.")
            response = JSONResponse (
                    status_code=status.HTTP_403_FORBIDDEN, 
                    content=error_response.dict())
            return response
   
    
    async def event_generator():
        last_created_at = None
        while True :
            notification_response: JSONResponse = await get_notification(user, page=0)
            if notification_response.status_code == 200:
                notification_res = json.loads(notification_response.body.decode('utf-8'))
                notifications = notification_res.get('data', [])
                # print("notifications:",notifications)
                
                if notifications:
                    for notification in notifications:
                        created_at = notification.get('created_at')
                        
                        if last_created_at is None or (created_at and created_at > last_created_at):
                            last_created_at = created_at
                            yield f"data: {json.dumps(notification)}\n\n"
            await asyncio.sleep(1)

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
