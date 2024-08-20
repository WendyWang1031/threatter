from fastapi import APIRouter, Depends
from model.model import *
from model.model_user import *
from controller.member import * 
from service.security import security_get_current_user

from fastapi.responses import JSONResponse

member_router = APIRouter()


# 用戶
@member_router.patch("/api/member",
        tags= ["Member"],
        response_model = SuccessfulRes , 
        summary = "編輯會員資料",
        responses = {
            200:{
                "model" : SuccessfulRes,
                "description" : "成功編輯會員資料"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_patch_member(member_update : MemberUpdateReq , 
                             current_user : Optional[dict] = Depends(security_get_current_user)) -> JSONResponse :
    return await update_member_data(member_update , current_user)

@member_router.get("/api/member/{account_id}",
        tags= ["Member"],
        response_model = MemberDetail ,
        summary = "顯示會員資料",
        responses = {
            200:{
                "model" : MemberDetail,
                "description" : "成功顯示會員資料"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_get_member(current_user :  Optional[dict] = Depends(security_get_current_user),
                        account_id: str = Path(..., description="該會員的帳號")) -> JSONResponse :
    return await get_member_data(current_user , account_id)
