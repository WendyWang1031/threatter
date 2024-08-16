import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.search import *
from service.security import security_get_current_user



async def get_search(search : str , 
                     page: int,
                     current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    try:

        if not current_user :
            error_response = ErrorResponse(error=True, message="User not authenticated")
            response = JSONResponse (
                status_code=status.HTTP_403_FORBIDDEN, 
                content=error_response.dict())
            return response
        
        member_id = current_user["account_id"]
       
        result = db_get_search(search , page , member_id)
        
        if result:
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=result.dict()
            )
            return response
        else:
            error_response = ErrorResponse(error=True, message="Failed to search")
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
    

