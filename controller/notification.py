import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.follow import *
from db.notification import *
from util.error_response import *



async def get_notification(current_user: dict ,  
                            page : int ,
                        ) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)
                                            
        result = db_get_notification(member_id , page, 15)
        if result is None:
            return data_not_found_error_response(DB_HAVE_NO_NOTIFICATION_DATA_ERROR)
        
        response = JSONResponse(
        status_code = status.HTTP_200_OK,
        content=result.dict()
        )
        return response
    
    except Exception as e :
        return interanal_server_error_response(str(e))

async def post_read_notification(current_time: datetime ,
                            current_user: dict 
                        ) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)

        
        result = db_post_read_notification(member_id , current_time)
        if result is None:
            return data_not_found_error_response(DB_HAVE_NO_NOTIFICATION_DATA_ERROR)

        response = JSONResponse(
        status_code = status.HTTP_200_OK,
        content = result)
        return response
    
    except Exception as e :
        return interanal_server_error_response(str(e))