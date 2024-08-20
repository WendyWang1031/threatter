from fastapi import APIRouter, Depends
from model.model import *
from model.model_user import *

from controller.comment import * 
from controller.like import * 

from service.security import security_get_current_user

from fastapi.responses import JSONResponse

comment_router = APIRouter()


# 留言
@comment_router.post("/api/member/{account_id}/post/{post_id}/comment/{comment_id}/like",
        tags= ["Comment"],
        response_model = LikeRes , 
        summary = "對貼文的某則留言按讚",
        responses = {
            200:{
                "model" : LikeRes,
                "description" : "成功對貼文的某則留言按讚"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_post_comments_like(
    comment_like : LikeReq,
    account_id : str = Path(..., description="該會員的帳號"),
    post_id : str = Path(..., description="該貼文的id"),
    comment_id : str = Path(..., description="該留言的id"),
    current_user : dict = Depends(security_get_current_user),
    ) -> JSONResponse :
    return await post_comment_or_reply_like(comment_like , account_id , post_id , comment_id , current_user)

@comment_router.post("/api/member/{account_id}/post/{post_id}/comment/{comment_id}/reply",
        tags= ["Comment"],
        response_model = Comment , 
        summary = "在貼文底下某則留言回覆留言",
        responses = {
            200:{
                "model" : Comment,
                "description" : "成功在某則貼文底下留言"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_post_comment_relpy(
    content_req:CommentReq,
    account_id: str = Path(..., description="該會員的帳號"),
    comment_id: str = Path(..., description="該留言的id"),
    current_user: Optional[dict] = Depends(security_get_current_user),
    ) -> JSONResponse :
    return await create_replies(content_req , comment_id , current_user)

@comment_router.delete("/api/member/{account_id}/post/{post_id}/comment/{comment_id}/reply",
        tags= ["Comment"],
        response_model = Comment , 
        summary = "刪除某則留言",
        responses = {
            200:{
                "model" : SuccessfulRes,
                "description" : "成功刪除某則留言"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_delete_comment(current_user : dict = Depends(security_get_current_user),
                                account_id: str = Path(..., description="該會員的帳號"),
                                post_id: str = Path(..., description="該貼文的id"),
                                comment_id: str = Path(..., description="該留言的id")
                                )-> JSONResponse :
    return await delete_comment_and_reply(comment_id , current_user)
