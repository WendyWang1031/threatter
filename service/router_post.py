from fastapi import APIRouter, Depends
from model.model import *
from model.model_user import *
from controller.post_new import * 
from controller.comment import * 
from controller.like import * 
from service.security import security_get_current_user

from fastapi.responses import JSONResponse

post_router = APIRouter()


# 貼文


@post_router.post("/api/post",
        tags= ["Post"],
        response_model = SuccessfulRes , 
        summary = "新增貼文",
        responses = {
            200:{
                "model" : SuccessfulRes,
                "description" : "成功新增貼文"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_post_post(create_post : PostCreateReq , 
                          current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    return await create_post_data(create_post , current_user)

@post_router.delete("/api/post/{post_id}",
        tags= ["Post"],
        response_model = SuccessfulRes , 
        summary = "刪除貼文",
        responses = {
            200:{
                "model" : SuccessfulRes,
                "description" : "成功刪除貼文"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_delete_post(
    post_id: str = Path(..., description="該貼文的id"), 
    current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    return await delete_post(post_id , current_user)

@post_router.get("/api/post/home",
        tags= ["Post"],
        response_model = PostListRes , 
        summary = "顯示首頁熱門貼文",
        responses = {
            200:{
                "model" : PostListRes,
                "description" : "成功顯示首頁熱門貼文"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_get_home_post(
    current_user: Optional[dict] = Depends(security_get_current_user),
    page: int = Query(0, description="下一頁的頁面，如果沒有更多頁為None")) -> JSONResponse :
    return await get_post_home(current_user , page)

@post_router.get("/api/post/home/recommendation",
        tags= ["Post"],
        response_model = PostListRes , 
        summary = "顯示首頁個人化與追蹤對象貼文",
        responses = {
            200:{
                "model" : PostListRes,
                "description" : "成功顯示首頁個人化與追蹤對象貼文"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_get_home_popular_post(
    current_user: dict = Depends(security_get_current_user),
    page: int = Query(0, description="下一頁的頁面，如果沒有更多頁為None")) -> JSONResponse :
    return await get_post_home_personalized_recommendations(current_user , page)

@post_router.get("/api/member/{account_id}/posts",
        tags= ["Post"],
        response_model = PostListRes , 
        summary = "顯示用戶檔案下方貼文",
        responses = {
            200:{
                "model" : PostListRes,
                "description" : "成功顯示單頁貼文"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_get_member_post(
    current_user: Optional[dict] = Depends(security_get_current_user),
    account_id: str = Path(..., description="該會員的帳號"),
    page: int = Query(0, description="頁碼")) -> JSONResponse :
    return await get_post_member_page(current_user, account_id, page)

@post_router.get("/api/member/{account_id}/post/{post_id}",
        tags= ["Post"],
        response_model = Post , 
        summary = "顯示單頁貼文",
        responses = {
            200:{
                "model" : Post,
                "description" : "成功顯示單頁貼文"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_get_single_post(
    current_user: Optional[dict] = Depends(security_get_current_user),
    account_id: str = Path(..., description="該會員的帳號") , 
    post_id: str = Path(..., description="該貼文的id")
    ) -> JSONResponse :
    return await get_post_single_page(current_user, account_id, post_id)

@post_router.get("/api/member/{account_id}/post/{post_id}/detail",
        tags= ["Post"],
        response_model = CommentDetailListRes ,
        summary = "顯示單頁貼文留言與留言回覆",
        responses = {
            200:{
                "model" : CommentDetailListRes,
                "description" : "成功顯示單頁貼文留言與留言回覆"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_get_comments_and_replies(
    current_user: Optional[dict] = Depends(security_get_current_user),
    account_id: str = Path(..., description="該會員的帳號"),
    post_id: str = Path(..., description="該貼文的id"),
    page: int = Query(0, description="頁碼")
) -> JSONResponse :
    return await get_comments_and_replies(current_user , account_id , post_id , page)


@post_router.post("/api/member/{account_id}/post/{post_id}/like",
        tags= ["Post"],
        response_model = LikeRes ,
        summary = "對貼文按讚",
        responses = {
            200:{
                "model" : LikeRes,
                "description" : "成功對貼文按讚"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_post_post_like(
    post_like : LikeReq ,
    account_id : str = Path(..., description="該會員的帳號"),
    post_id : str = Path(..., description="該貼文的id"),
    current_user : dict = Depends(security_get_current_user),
    ) -> JSONResponse :
    return await post_post_like(post_like , account_id , post_id , current_user)

@post_router.post("/api/member/{account_id}/post/{post_id}/reply",
        tags= ["Post"],
        response_model = SuccessfulRes , 
        summary = "在某則貼文底下留言",
        responses = {
            200:{
                "model" : SuccessfulRes,
                "description" : "成功在某則貼文底下留言"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_post_comment(content_req: CommentReq ,
                            account_id: str = Path(..., description="該會員的帳號"),
                            post_id: str = Path(..., description="該貼文的id"),
                            current_user: Optional[dict] = Depends(security_get_current_user),
                            
                             ) -> JSONResponse :
    return await create_comments(content_req , account_id , post_id , current_user)

