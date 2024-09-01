import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.comment import *
from db.post_new import *
from db.update_counts import *
from util.error_response import *
from service.security import security_get_current_user


async def create_comments(content_data : CommentReq , 
                        account_id: str, 
                        post_id : str ,
                        current_user : dict = Depends(security_get_current_user),
                        ) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)

        if not content_data.content.text and not (content_data.content.media and (content_data.content.media.images or content_data.content.media.videos or content_data.content.media.audios)):
            return bad_request_error_response(FAILED_UPDATE_COMMENT_DATA_FIELD_EMPTY_ERROR) 
        
        result = await db_create_comment_data(content_data , account_id , post_id , member_id)
        if result is False:
            return bad_request_error_response(FAILED_UPDATE_DATA_ERROR) 
        
        return successful_response()

    except Exception as e :
        return interanal_server_error_response(str(e))
    

async def create_replies(content_data : CommentReq , 
                        account_id: str,
                        post_id : str ,  
                        comment_id : str ,
                        current_user : dict = Depends(security_get_current_user),
                        ) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)

        if not content_data.content.text and not (content_data.content.media and (content_data.content.media.images or content_data.content.media.videos or content_data.content.media.audios)):
            return bad_request_error_response(FAILED_UPDATE_REPLY_DATA_FIELD_EMPTY_ERROR) 
 
        result =await db_create_reply_data(content_data , account_id , post_id , comment_id , member_id)
        if result is False:
            return bad_request_error_response(FAILED_UPDATE_DATA_ERROR)
        
        return successful_response()

    except Exception as e :
        return interanal_server_error_response(str(e))
       
async def delete_comment_and_reply(comment_id : str ,
                                current_user : dict = Depends(security_get_current_user)
                                   ) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)
        
        delete_post_result = db_delete_comment_and_reply(comment_id , member_id)            
        if delete_post_result is False:
            return bad_request_error_response(FAILED_DELETE_DATA_ERROR) 
        
        return successful_response()    
        
    except Exception as e :
        return interanal_server_error_response(str(e))


async def get_comments_and_replies(current_user: Optional[dict], account_id: str , post_id : str , page: int) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        result , comments_data = db_get_comments_and_replies_data(member_id , account_id , post_id , page)
        
        if result == "No Comment Data" :
            return bad_request_error_response(FAILED_GET_COMMENT_DATA_ERROR) 
        
        elif result == "Success" :
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=json.loads(comments_data.json())
            )
            return response
            
        else:
            return data_not_found_error_response(DB_HAVE_NO_COMMENT_DATA_ERROR)

    except Exception as e :
        return interanal_server_error_response(str(e))
  

