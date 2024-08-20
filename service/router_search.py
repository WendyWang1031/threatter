from fastapi import APIRouter, Depends
from model.model import *
from model.model_user import *
from controller.search import * 
from service.security import security_get_current_user

from fastapi.responses import JSONResponse

search_router = APIRouter()

# 搜尋
@search_router.get("/api/search",
        tags= ["Search"],
        response_model = FollowMemberListRes , 
        summary = "搜尋用戶帳號",
        responses = {
            200:{
                "model" : FollowMemberListRes,
                "description" : "成功搜尋用戶帳號"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_search(
    search: str = Query(..., description="輸入想要搜尋的帳號"), 
    page: int = Query(0, description="下一頁的頁面，如果沒有更多頁為None"),
    current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    return await get_search(search , page , current_user)
