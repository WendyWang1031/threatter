from fastapi import APIRouter, Depends
from model.model import *
from model.model_user import *
from controller.user import * 
from service.security import security_get_current_user

from fastapi.responses import JSONResponse

user_router = APIRouter()

# # 搜尋
# @search_router.get("/api/search",
#         tags= ["Search"],
#         response_model = FollowMemberListRes , 
#         summary = "搜尋用戶帳號",
#         responses = {
#             200:{
#                 "model" : FollowMemberListRes,
#                 "description" : "成功搜尋用戶帳號"
#             },
#             500:{
#                 "model" : ErrorResponse,
#                 "description" : "伺服器內部錯誤"
#             }
#          })
# async def fetch_search(
#     search: str = Query(..., description="輸入想要搜尋的帳號"), 
#     page: int = Query(0, description="下一頁的頁面，如果沒有更多頁為None"),
#     current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
#     return await get_search(search , page , current_user)


# @app.post("/api/user" , 
#          tags= ["User"],
#          response_model = UserPutReq ,
#          summary = "註冊一個新會員",
        
#          responses = {
#             200:{
#                 "model" : SuccessfulResponseForRegister,
#                 "description" : "註冊成功"
#             },
#             400:{
#                 "model" : ErrorResponse,
#                 "description" : "註冊失敗，重複的 Email 或其他原因"
#             },
#             500:{
#                 "model" : ErrorResponse,
#                 "description" : "伺服器內部錯誤"
#             }
#          })
# async def fetch_post_user_signup(user_request : UserRegisterReq) -> JSONResponse :
#     return await register_user(user_request)

#會員
@user_router.post("/api/user" , 
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

@user_router.get("/api/user/auth" , 
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

@user_router.put("/api/user/auth" , 
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
