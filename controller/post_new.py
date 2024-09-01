import boto3
import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.post_new import *
from db.check_relation import *
from db.check_post import *
from db.update_counts import *
from service.security import security_get_current_user
from datetime import datetime
from util.error_response import *
from service.redis import RedisManager

from datetime import datetime

def convert_datetime_to_string(dt: datetime) -> str:
    return dt.isoformat()

def convert_post_data(post_data):
    if 'data' in post_data and isinstance(post_data['data'], list):
        # print("post_data['data']:",post_data['data'])
        for post in post_data['data']:
            if 'created_at' in post and isinstance(post['created_at'], datetime):
                post['created_at'] = convert_datetime_to_string(post['created_at'])
    return post_data

async def create_post_data(post_data : PostCreateReq , current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)

        if not post_data.content.text and not (post_data.content.media and (post_data.content.media.images or post_data.content.media.videos or post_data.content.media.audios)):
            return bad_request_error_response(FAILED_UPDATE_POST_DATA_FIELD_EMPTY_ERROR) 

        member_id = current_user["account_id"]    
        result , post_id = db_create_post_data(post_data , member_id)
        if result is None:
            return bad_request_error_response(FAILED_UPDATE_POST_DATA_FIELD_EMPTY_ERROR) 

        else :
            success_response = SuccessfulRes(success=True, post_id = post_id)
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=success_response.dict() 
            )
            return response

    except Exception as e :
        return interanal_server_error_response(str(e))
    
    
async def get_post_home(current_user: Optional[dict], page: int) -> JSONResponse :
    try:
        
        member_id = current_user["account_id"] if current_user else None
        
        cached_posts, cached_next_page = await RedisManager.get_popular_posts(page)
        # print("posts_to_cache:",cached_posts)
        if cached_posts:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "cached": True,
                    "next_page": cached_next_page,
                    "data": cached_posts
                }
            )
        
        post_data = db_get_popular_posts(member_id , 60 , page)
        print(f"post_data type: {type(post_data)}, content: {post_data}")
        
        if post_data :
            posts_to_cache = post_data.dict() if hasattr(post_data, 'dict') else post_data
            # print(f"posts_to_cache before type: {type(posts_to_cache)}, content: {posts_to_cache}")
            posts_to_cache = convert_post_data(posts_to_cache)
            # print(f"posts_to_cache after type: {type(posts_to_cache)}, content: {posts_to_cache}")

            await RedisManager.cache_popular_posts(page, posts_to_cache)

            next_page = posts_to_cache.get("next_page")
            data_to_cache = posts_to_cache.get("data", [])
            
            # print("without cache posts_to_cache:",posts_to_cache)
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content={
                    "cached": False,
                    "next_page": next_page,
                    "data": data_to_cache
                }
            )
            return response
            
        else:
            return data_not_found_error_response(FAILED_GET_POST_DATA_ERROR)

        
    except Exception as e :
        return interanal_server_error_response(str(e))
    
async def get_post_home_personalized_recommendations(
        current_user: dict, page: int) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)
        
        post_data = db_get_personalized_recommendations(member_id , page)
        
        if post_data :
            
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=json.loads(post_data.json())
            )
            return response
            
        else:
            return bad_request_error_response(FAILED_GET_POST_DATA_ERROR) 

    except Exception as e :
        return interanal_server_error_response(str(e))
    
async def delete_post(post_id : str , current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)
        
        post_exist_result = db_check_post_exist_or_not(member_id , post_id)
        if post_exist_result is False:
            return data_not_found_error_response(FAILED_DELETE_POST_DATA_ERROR)

        delete_post_result = db_delete_post(post_id , member_id)

        if delete_post_result is None:
            bad_request_error_response(FAILED_DELETE_DATA_ERROR)
        else:
            return successful_response()
       
    except Exception as e :
        return interanal_server_error_response(str(e))


async def get_post_member_page(current_user: Optional[dict], account_id: str , page: int) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        
        relation = db_check_member_target_relation(member_id , account_id) 

        if relation is False:
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)
        
        elif relation is True:
            post_data = db_get_member_post_data(member_id , account_id , page)
            if post_data: 
                response = JSONResponse(
                    status_code = status.HTTP_200_OK,
                    content = json.loads(post_data.json())
                )
                return response
            else:
                return bad_request_error_response(FAILED_GET_MEMBER_POST_DATA_ERROR)

        
    except Exception as e :
        return interanal_server_error_response(str(e))
  

async def get_post_single_page(current_user: Optional[dict], account_id: str , post_id : str) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None

        relation = db_check_member_target_relation(member_id , account_id) 
         
        if relation is None:
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)
        
        post_exist_result = db_check_post_exist_or_not(account_id , post_id)
        if post_exist_result is False:
            return data_not_found_error_response(FAILED_GET_POST_DATA_ERROR)
        
        
        post_data = db_get_single_post_data(member_id , account_id , post_id)
        if post_data: 
            response = JSONResponse(
                status_code = status.HTTP_200_OK,
                content = json.loads(post_data.json())
            )
            return response

        else:
            return bad_request_error_response(FAILED_GET_MEMBER_POST_DATA_ERROR)
  
    except Exception as e :
        return interanal_server_error_response(str(e))
