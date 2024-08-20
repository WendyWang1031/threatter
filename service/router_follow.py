from fastapi import APIRouter, Depends
from model.model import *
from model.model_user import *
from controller.follow import * 
from controller.comment import * 

from service.security import security_get_current_user

from fastapi.responses import JSONResponse

follow_router = APIRouter()


# 追蹤
@follow_router.post("/api/follow",
        tags= ["Follow"],
        response_model = FollowMember , 
        summary = "追蹤對方",
        responses = {
            200:{
                "model" : FollowMember,
                "description" : "成功追蹤對方"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_post_follow(follow : FollowReq,
                            current_user : dict = Depends(security_get_current_user)
                            ) -> JSONResponse :
    return await post_follow_target(follow , current_user)

@follow_router.post("/api/follow/member/follow",
        tags= ["Follow"],
        response_model = FollowMember , 
        summary = "私人用戶回應追蹤",
        responses = {
            200:{
                "model" : FollowMember,
                "description" : "私人用戶回應追蹤對方"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_post_private_follow(followAns : FollowAns,
                                    current_user : dict = Depends(security_get_current_user)
                            ) -> JSONResponse :
    return await post_private_user_res_follow(followAns , current_user)

@follow_router.get("/api/follow/member/follow",
        tags= ["Follow"],
        response_model = FollowMemberListRes , 
        summary = "私人用戶：顯示要求追蹤的對象",
        responses = {
            200:{
                "model" : FollowMemberListRes,
                "description" : "成功顯示要求追蹤的對象"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_get_pending_target(
    current_user :  dict = Depends(security_get_current_user),
    page: int = Query(0, description="下一頁的頁面，如果沒有更多頁為None")
    ) -> JSONResponse :
    return await get_pending_target(current_user , page)


@follow_router.get("/api/member/{account_id}/follow/target",
        tags= ["Follow"],
        response_model = FollowMemberListRes , 
        summary = "顯示追蹤中對象",
        responses = {
            200:{
                "model" : FollowMemberListRes,
                "description" : "成功顯示顯示追蹤中對象"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_get_follow_target(
    current_user :  Optional[dict] = Depends(security_get_current_user),
    account_id: str = Path(..., description="該會員的帳號"),
    page: int = Query(0, description="下一頁的頁面，如果沒有更多頁為None")
    ) -> JSONResponse :
    return await get_follow_target(current_user , account_id , page)

@follow_router.get("/api/member/{account_id}/follow/fans",
        tags= ["Follow"],
        response_model = FollowMemberListRes ,
        summary = "顯示追蹤本人的粉絲",
        responses = {
            200:{
                "model" : FollowMemberListRes,
                "description" : "成功顯示追蹤本人的粉絲"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_get_follow_fans(
    current_user :  Optional[dict] = Depends(security_get_current_user),
    account_id: str = Path(..., description="該會員的帳號"),
    page: int = Query(0, description="下一頁的頁面，如果沒有更多頁為None")
    ) -> JSONResponse :
    return await get_follow_fans(current_user , account_id , page)
