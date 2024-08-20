from fastapi import *
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse , JSONResponse
from service.security import security_get_current_user
from typing import Optional
from model.model import *
import asyncio

notification_router = APIRouter()

@notification_router.get("/notification" , tags=["Notification"])
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