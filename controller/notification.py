import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.follow import *

from db.notification import *


async def get_notification(current_user: dict ,  
                            page : int ,
                        ) -> JSONResponse :
    try:
    
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            error_response = ErrorResponse(error=True, message="User not authenticated")
            response = JSONResponse (
                    status_code=status.HTTP_403_FORBIDDEN, 
                    content=error_response.dict())
            return response

        
        result = db_get_notification(member_id , page)
        if result is None:
            error_response = ErrorResponse(error=True, message="該用戶並無權限調閱")
            response = JSONResponse (
                status_code=status.HTTP_403_FORBIDDEN, 
                content=error_response.dict())
            return response
        

        response = JSONResponse(
        status_code = status.HTTP_200_OK,
        content=result.dict()
        )
        return response

    
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response


