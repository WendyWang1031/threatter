from fastapi import *
from fastapi import  Depends
from fastapi.responses import JSONResponse

from model.model import *
from util.error_response import *
from service.security import security_get_current_user
from db.member import *

async def update_member_data(
        member_data: MemberUpdateReq ,
        current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)

        fields_updated = False
        if (member_data.name and member_data.name.strip()) or \
            (member_data.visibility and member_data.visibility.strip()) or \
            (member_data.self_intro and member_data.self_intro.strip()) or \
            (member_data.avatar and member_data.avatar.strip()):
                fields_updated = True

        if not fields_updated:
            return bad_request_error_response(FAILED_UPDATE_MEMBER_DATA_FIELD_EMPTY_ERROR) 
        
        result = db_update_member_data(member_id , member_data)
        if result is False:
            return bad_request_error_response(FAILED_UPDATE_DATA_ERROR) 
        
        return successful_response()

    except Exception as e :
        return interanal_server_error_response(str(e))
    
    
async def get_member_data(current_user: Optional[dict] , account_id : str ) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        member_detail = db_get_member_data(member_id , account_id)
        if member_detail is None:
            return bad_request_error_response(FAILED_GET_DATA_ERROR) 
            
        response = JSONResponse(
        status_code = status.HTTP_200_OK,
        content=member_detail.dict()
        )
        return response

    except Exception as e :
        return interanal_server_error_response(str(e))