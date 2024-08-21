from fastapi import *
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse , JSONResponse
from service.security import security_get_current_user
from typing import Optional
from model.model import *
from controller.notification import *
import asyncio

notification_router = APIRouter()

@notification_router.get("/api/notification/stream" , tags=["Notification"])
async def stream_notification(current_user: dict = Depends(security_get_current_user)):
    
    if not current_user :
            error_response = ErrorResponse(error=True, message="User not authenticated")
            response = JSONResponse (
                    status_code=status.HTTP_403_FORBIDDEN, 
                    content=error_response.dict())
            return response
    member_id = current_user["account_id"]   
    
    async def event_generator():
        while True :
            notifications = []
            if notifications:
                for notification in notifications :
                    pass
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
async def fetch_get_follow_fans(
    current_user :  Optional[dict] = Depends(security_get_current_user),
    page: int = Query(0, description="下一頁的頁面，如果沒有更多頁為None")
    ) -> JSONResponse :
    return await get_notification(current_user , page)
