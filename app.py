from fastapi import *
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer
from fastapi.responses import FileResponse ,RedirectResponse


from controller.post import * 
from controller.post_new import * 
from controller.generate_presigned import * 
from controller.user import *
from controller.member import *
from controller.comment import *
from controller.like import *
from controller.follow import *

from model.model import *
from model.model_user import *
from service.security import security_get_current_user
from service.presigned_url import *




app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
security = HTTPBearer(auto_error=False)  

def get_token(authorization: str = Header(...)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    return authorization

def get_optional_token(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    return authorization

# 測試版－作業－貼文
@app.post("/api/post/generate-presigned-url_test",
        tags= ["Post-Test"], 
        summary = "S3 產生欲簽名 URL",
         )
async def fetch_post_generate_presigned_url_test(presignedUrl_request: PresignedUrlRequest) -> JSONResponse :
    print("presignedUrl_request:", presignedUrl_request)
    return await generate_presigned_url(presignedUrl_request.file_name , presignedUrl_request.file_type)

@app.post("/api/post_test",
        tags= ["Post-Test"],
        response_model = PostGetResponse , 
        summary = "新增貼文資料",
        responses = {
            200:{
                "model" : PostGetResponse,
                "description" : "修改成功"
            },
            400:{
                "model" : ErrorResponse,
                "description" : "修改失敗，輸入不正確或其他原因"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         }
         )
async def fetch_post_post_test(post_data : PostData) -> JSONResponse :
    return await create_post_data(post_data)

@app.get("/api/post_test",
        tags= ["Post-Test"],
        response_model = PostGetResponse , 
        summary = "根據id取得貼文資訊",
        responses = {
            200:{
                "model" : PostGetResponse,
                "description" : "成功取得貼文資料"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_get_post_test() -> JSONResponse :
    return await get_post_data()

# 共用
@app.post("/api/post/generate-presigned-url",
        tags= ["Common"], 
        summary = "S3 產生欲簽名 URL",
         )
async def fetch_post_generate_presigned_url(presignedUrl_request: PresignedUrlRequest) -> JSONResponse :
    return await generate_presigned_url(presignedUrl_request.file_name , presignedUrl_request.file_type)


# 會員
@app.patch("/api/member",
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

@app.get("/api/member/{account_id}",
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
async def fetch_get_member(account_id: str = Path(..., description="該會員的帳號")) -> JSONResponse :
    return await get_member_data(account_id)

# 追蹤
@app.post("/api/follow",
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
    return await follow_target(follow , current_user)

@app.get("/api/member/{account_id}/follow/target",
        tags= ["Follow"],
        response_model = FollowMemberListRes , 
        dependencies=[Depends(get_optional_token)], 
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
    account_id: str = Path(..., description="該會員的帳號"),
    page: int = Query(0, description="下一頁的頁面，如果沒有更多頁為None")
    ) -> JSONResponse :
    pass

@app.get("/api/member/{account_id}/follow/fans",
        tags= ["Follow"],
        response_model = FollowMemberListRes ,
        dependencies=[Depends(get_optional_token)], 
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
    account_id: str = Path(..., description="該會員的帳號"),
    page: int = Query(0, description="下一頁的頁面，如果沒有更多頁為None")
    ) -> JSONResponse :
    pass

# 貼文


@app.post("/api/post",
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

@app.delete("/api/post/{post_id}",
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

@app.get("/api/post/home",
        tags= ["Post"],
        response_model = PostListRes , 
        summary = "顯示首頁貼文",
        responses = {
            200:{
                "model" : PostListRes,
                "description" : "成功顯示首頁貼文"
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

@app.get("/api/member/{account_id}/posts",
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

@app.get("/api/member/{account_id}/post/{post_id}",
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

@app.get("/api/member/{account_id}/post/{post_id}/detail",
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


@app.post("/api/member/{account_id}/post/{post_id}/like",
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
    return await post_post_like(post_like , post_id , current_user)

@app.post("/api/member/{account_id}/post/{post_id}/reply",
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
    return await create_comments(content_req , post_id , current_user)




# 留言
@app.post("/api/member/{account_id}/post/{post_id}/comment/{comment_id}/like",
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
    return await post_comment_or_reply_like(comment_like , comment_id , current_user)

@app.post("/api/member/{account_id}/post/{post_id}/comment/{comment_id}/reply",
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

@app.delete("/api/member/{account_id}/post/{post_id}/comment/{comment_id}/reply",
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


# 搜尋
@app.get("/api/search",
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
    page: int = Query(0, description="下一頁的頁面，如果沒有更多頁為None")) -> JSONResponse :
    pass

# 用戶
@app.post("/api/user" , 
         tags= ["User"],
         response_model = UserPutReq ,
         summary = "註冊一個新會員",
        
         responses = {
            200:{
                "model" : SuccessfulResponseForRegister,
                "description" : "註冊成功"
            },
            400:{
                "model" : ErrorResponse,
                "description" : "註冊失敗，重複的 Email 或其他原因"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_post_user_signup(user_request : UserRegisterReq) -> JSONResponse :
    return await register_user(user_request)

@app.get("/api/user/auth" , 
         tags= ["User"],
         response_model = UserGetCheck ,
         summary = "取得當前的登入資訊",
        
         responses = {
            200:{
                "model" : UserGetCheck,
                "description" : "已登入的會員資料，null 表示未登入"
            }
         })
async def fetch_get_user(user: UserGetCheck = Depends(security_get_current_user) )-> JSONResponse :
    return await get_user_details(user)

@app.put("/api/user/auth" , 
         tags= ["User"],
         response_model = UserPutReq ,
         summary = "登入會員帳戶",
        
         responses = {
            200:{
                "model" : Token,
                "description" : "登入成功，取得有效期為七天的 JWT 加密字串"
            },
            400:{
                "model" : ErrorResponse,
                "description" : "登入失敗，帳號或密碼錯誤或其他原因"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_put_user_signin(user_login_request : UserPutReq) -> JSONResponse :
    return await authenticate_user(user_login_request)

# ----------------------------------------------------------


# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
    return FileResponse("./static/index.html", media_type="text/html")

@app.get("/member/{account_id}", include_in_schema=False)
async def member(request: Request):
    return FileResponse("./static/member.html", media_type="text/html")

@app.get("/member/{account_id}/post/{post_id}", include_in_schema=False)
async def member(request: Request):
    return FileResponse("./static/single_page.html", media_type="text/html")

@app.get("/member")
async def redirect_to_home(request: Request):
    return RedirectResponse(url="/")
 