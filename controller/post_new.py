import boto3
import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.post_new import *
from db.check_relation import *
from db.check_post import *
from service.security import security_get_current_user


async def create_post_data(post_data : PostCreateReq , current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    try:
        if not current_user :
            error_response = ErrorResponse(error=True, message="User not authenticated")
            response = JSONResponse (
                    status_code=status.HTTP_403_FORBIDDEN, 
                    content=error_response.dict())
            return response

        if not post_data.content.text and not (post_data.content.media and (post_data.content.media.images or post_data.content.media.videos or post_data.content.media.audios)):
            error_response = ErrorResponse(error=True, message="請至少要提供文字或圖片")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response

        member_id = current_user["account_id"]    
        result = db_create_post_data(post_data , member_id)
        
        if result is True:
            success_response = SuccessfulRes(success=True)
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=success_response.dict()
            )
            return response
        else:
            error_response = ErrorResponse(error=True, message="Failed to create post data")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response

    
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response
    
    
async def get_post_home(current_user: Optional[dict], page: int) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        post_data = db_get_home_post_data(member_id , page)
        
        if post_data :
            
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=json.loads(post_data.json())
            )
            return response
            
        else:
            error_response = ErrorResponse(error=True, message="No post Data details found for user")
            response = JSONResponse (
                status_code=status.HTTP_404_NOT_FOUND, 
                content=error_response.dict())
            return response

        
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response
    
async def delete_post(post_id : str , current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    try:
        if not current_user :
            error_response = ErrorResponse(error=True, message="User not authenticated")
            response = JSONResponse (
                status_code=status.HTTP_403_FORBIDDEN, 
                content=error_response.dict())
            return response
        
        member_id = current_user["account_id"]

        post_exist_result = db_check_post_exist_or_not(member_id , post_id)
        if post_exist_result is False:
            error_response = ErrorResponse(error=True, message="資料庫並不存在該貼文資料")
            response = JSONResponse (
                status_code=status.HTTP_404_NOT_FOUND, 
                content=error_response.dict())
            return response

        delete_post_result = db_delete_post(post_id , member_id)
            
        if delete_post_result:
            success_response = SuccessfulRes(success=True)
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=success_response.dict()
            )
            return response
        else:
            response = JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": True,
                    "message": str(e)
                })
            return response
        
            
            
        
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response


async def get_post_member_page(current_user: Optional[dict], account_id: str , page: int) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        
        relation = db_check_member_target_relation(member_id , account_id) 

        if relation is None:
            error_response = ErrorResponse(error=True, message="該用戶並無權限調閱")
            response = JSONResponse (
                status_code=status.HTTP_403_FORBIDDEN, 
                content=error_response.dict())
            return response
        
        elif relation is True:
            post_data = db_get_member_post_data(account_id , page)
            if post_data: 
                response = JSONResponse(
                    status_code = status.HTTP_200_OK,
                    content = json.loads(post_data.json())
                )
                return response
            else:
                error_response = ErrorResponse(error=True, message="No member's post data found")
                response = JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    content=error_response.dict()
                )
                return response

        
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response
  

async def get_post_single_page(current_user: Optional[dict], account_id: str , post_id : str) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None

        relation = db_check_member_target_relation(member_id , account_id) 
         
        if relation is None:
            error_response = ErrorResponse(error=True, message="該用戶並無權限調閱")
            response = JSONResponse (
                status_code=status.HTTP_403_FORBIDDEN, 
                content=error_response.dict())
            return response
        
        elif relation is True:
            post_data = db_get_single_post_data(account_id , post_id)
            if post_data: 
                response = JSONResponse(
                    status_code = status.HTTP_200_OK,
                    content = json.loads(post_data.json())
                )
                return response
            else:
                error_response = ErrorResponse(error=True, message="No post data found")
                response = JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    content=error_response.dict()
                )
                return response
        else:
            error_response = ErrorResponse(error=True, message="Failed to get member's single post")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response

        
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response
