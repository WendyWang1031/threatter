import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.like import *
from db.check_relation import *
from db.check_post import *
from service.security import security_get_current_user


async def post_post_like(post_like : LikeReq , 
                        account_id : str, 
                        post_id : str ,
                        current_user : dict = Depends(security_get_current_user),
                        ) -> JSONResponse :
    try:
        if not current_user :
            error_response = ErrorResponse(error=True, message="User not authenticated")
            response = JSONResponse (
                    status_code=status.HTTP_403_FORBIDDEN, 
                    content=error_response.dict())
            return response

        member_id = current_user["account_id"] 

        target_exist_result = db_check_target_exist_or_not(account_id)
        if target_exist_result is False:
            error_response = ErrorResponse(error=True, message="資料庫並不存在該用戶資料")
            response = JSONResponse (
                status_code=status.HTTP_404_NOT_FOUND, 
                content=error_response.dict())
            return response
        
        post_exist_result = db_check_post_exist_or_not(account_id , post_id)
        if post_exist_result is False:
            error_response = ErrorResponse(error=True, message="資料庫並不存在該貼文資料")
            response = JSONResponse (
                status_code=status.HTTP_404_NOT_FOUND, 
                content=error_response.dict())
            return response


        result = db_like_post(post_like , post_id , member_id)
        if result:
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=result.dict()
            )
            return response
        else:
            error_response = ErrorResponse(error=True, message="Failed to update like data")
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
    

async def post_comment_or_reply_like(comment_like : LikeReq ,  
                                    comment_id : str ,
                                    current_user : dict = Depends(security_get_current_user),
                        ) -> JSONResponse :
    try:
        if not current_user :
            error_response = ErrorResponse(error=True, message="User not authenticated")
            response = JSONResponse (
                    status_code=status.HTTP_403_FORBIDDEN, 
                    content=error_response.dict())
            return response

        member_id = current_user["account_id"]    
        result = db_like_comment_or_reply(comment_like , comment_id , member_id)
        
        if result:
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=result.dict()
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
  
