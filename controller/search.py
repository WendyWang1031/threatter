import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.search import *



async def get_search(search: str , page: int) -> JSONResponse :
    try:
       
        result = db_get_search(search , page)
        
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
    

