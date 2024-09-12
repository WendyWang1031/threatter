import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.like import *
from db.check_relation import *
from db.check_post import *
from db.update_counts import *
from util.error_response import *
from service.redis import RedisManager
from service.security import security_get_current_user

async def post_post_like(post_like : LikeReq , 
                        account_id : str, 
                        post_id : str ,
                        current_user : dict = Depends(security_get_current_user),
                        ) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)

        check_results = db_check_existence_and_relations(account_id, post_id, member_id)
        if not check_results.get("user_exists"):
            return data_not_found_error_response(DB_HAVE_NO_USER_DATA_ERROR)
        
        if post_id and not check_results.get("post_exists"):
            return data_not_found_error_response(DB_HAVE_NO_POST_DATA_ERROR)

        result = await db_like_post(account_id , post_like , post_id , member_id)        
        if result is False:
            return bad_request_error_response(FAILED_UPDATE_DATA_ERROR)
        
        # 創建 Redis 連線管理器
        await RedisManager.init_redis()
        redis_client = RedisManager.get_redis()
        # 加權按讚分數  
        await redis_client.zincrby('popular_posts_zset', 2, post_id)

        result = (LikeRes(total_likes = result)).dict()
        response = JSONResponse(
        status_code = status.HTTP_200_OK,
        content = result
        )
        return response

    except Exception as e :
        return interanal_server_error_response(str(e))
    
async def post_comment_or_reply_like(comment_like : LikeReq ,
                                    account_id : str, 
                                    post_id : str ,  
                                    comment_id : str ,
                                    current_user : dict = Depends(security_get_current_user),
                        ) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)

        check_results = db_check_existence_and_relations(account_id, post_id, comment_id, member_id)
        if not check_results.get("user_exists"):
            return data_not_found_error_response(DB_HAVE_NO_USER_DATA_ERROR)
        
        if post_id and not check_results.get("post_exists"):
            return data_not_found_error_response(DB_HAVE_NO_POST_DATA_ERROR)
        
        if comment_id and not check_results.get("comment_exists") and not check_results.get("reply_exists"):
            return data_not_found_error_response(DB_HAVE_NO_COMMENT_DATA_ERROR)
        
        result = await db_like_comment_or_reply(account_id , post_id , comment_like , comment_id , member_id)
        if result is False:
            return bad_request_error_response(FAILED_UPDATE_DATA_ERROR)
        
        result = (LikeRes(total_likes = result)).dict()
        response = JSONResponse(
        status_code = status.HTTP_200_OK,
        content = result
        )
        return response

    except Exception as e :
        return interanal_server_error_response(str(e))
  
