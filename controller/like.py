import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.like import *
from service.security import security_get_current_user


async def post_post_like(post_like : LikeReq ,  
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
        result = db_like_post(post_like , post_id , member_id)
        
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
    

async def create_replies(content_data : CommentReq ,  
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

        if not content_data.content.text and not (content_data.content.media and (content_data.content.media.images or content_data.content.media.videos or content_data.content.media.audios)):
            error_response = ErrorResponse(error=True, message="請至少要提供文字或圖片")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response

        member_id = current_user["account_id"]    
        result = db_create_reply_data(content_data , comment_id , member_id)
        
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
       
async def delete_comment_and_reply(comment_id : str ,
                                current_user : dict = Depends(security_get_current_user)
                                   ) -> JSONResponse :
    try:
        if current_user :
            member_id = current_user["account_id"]
            delete_post_result = db_delete_comment_and_reply(comment_id , member_id)
            
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
        else:
            error_response = ErrorResponse(error=True, message="User not authenticated")
            response = JSONResponse (
                status_code=status.HTTP_403_FORBIDDEN, 
                content=error_response.dict())
            return response
            
        
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response


async def get_comments_and_replies(current_user: Optional[dict], account_id: str , post_id : str , page: int) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        comments_data = db_get_comments_and_replies_data(member_id , account_id , post_id , page)
        
        if comments_data :
            
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=json.loads(comments_data.json())
            )
            return response
            
        else:
            error_response = ErrorResponse(error=True, message="No member's comments data details found for user")
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
  

async def get_post_single_page(current_user: Optional[dict], account_id: str , post_id : str) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        post_data = db_get_single_post_data(member_id , account_id , post_id)
        
        if post_data :
            
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=json.loads(post_data.json())
            )
            return response
            
        else:
            error_response = ErrorResponse(error=True, message="No member's post data details found for user")
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
