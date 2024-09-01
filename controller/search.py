import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.search import *
from util.error_response import *
from service.security import security_get_current_user

async def get_search(search : str , 
                     page: int,
                     current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)

        result = db_get_search(search , page , member_id)
        if result is None:
            return bad_request_error_response(FAILED_GET_DATA_ERROR)
            
        response = JSONResponse(
        status_code = status.HTTP_200_OK,
        content=result.dict()
        )
        return response

    except Exception as e :
        return interanal_server_error_response(str(e))
