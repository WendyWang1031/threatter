import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.follow import *
from db.check_relation import *
from db.get_member_data import *
from util.error_response import *
from service.security import security_get_current_user


async def post_follow_target(followReq : FollowReq , 
                        current_user : dict = Depends(security_get_current_user),
                        ) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)    

        relation = db_check_each_other_relation(member_id , followReq.account_id)
        if followReq.follow is True and relation == "Following" :
            return bad_request_error_response(FAILED_GET_FOLLOW_DATA_ERROR)
       
       
        relation_state , insert_result = await db_follow_target(followReq , member_id)
        if insert_result is False:
            return bad_request_error_response(FAILED_UPDATE_FOLLOW_PRIVATE_DATA_ERROR)

        
        follow_member_data = db_get_member_single_data(followReq.account_id, relation_state)
        if follow_member_data is False:
            return bad_request_error_response(FAILED_GET_DATA_ERROR)
        
        else:
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=follow_member_data.dict()
            )
            return response

    
    except Exception as e :
        return interanal_server_error_response(str(e))
    
'''
def update_notification(
        member_id: str, 
        account_id: str, 
        action_type: str):
    
    db_update_notification(
                    member_id, follow.account_id , None , None , 'Follow' , None , False , follow_status)

    await RedisManager.publish_notification(notification, account_id)
'''



async def post_private_user_res_follow(followAns : FollowAns ,
                            current_user : dict = Depends(security_get_current_user),
                        ) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        if member_id is None :
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)    
   

        relation = db_check_each_other_relation(member_id , followAns.account_id)
        
        if followAns.accept is True and relation == "Following" :
            return bad_request_error_response(FAILED_GET_FOLLOW_DATA_ERROR)
          
        
        relation_state , insert_result = await db_private_user_res_follow(followAns , followAns.account_id , member_id)
        
        if insert_result is False:
            return bad_request_error_response(FAILED_UPDATE_FOLLOW_PRIVATE_DATA_ERROR)

        # db get FollowMember
        follow_member_data = db_get_member_single_data(followAns.account_id, relation_state)
        
        if follow_member_data is False:
            return bad_request_error_response(FAILED_GET_DATA_ERROR)

        else :
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=follow_member_data.dict()
            )
            return response

    
    except Exception as e :
        return interanal_server_error_response(str(e))


async def get_pending_target(current_user: dict ,  
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
        
        # db get user 
        # check success or fail
        
        result = db_get_pending_target(member_id , page)
        if result is False:
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
        return interanal_server_error_response(str(e))

async def get_follow_target(current_user: Optional[dict] ,  
                            account_id : str ,
                            page : int ,
                        ) -> JSONResponse :
    try:
    
        member_id = current_user["account_id"] if current_user else None

        target_exist_result = db_check_target_exist_or_not(account_id)
        if target_exist_result is False:
            return data_not_found_error_response(DB_HAVE_NO_USER_DATA_ERROR)
        
        
        relation = db_check_member_target_relation(member_id , account_id)  
        if relation is False:
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)
        
        
        result = db_get_follow_target(member_id , account_id , page)
        response = JSONResponse(
        status_code = status.HTTP_200_OK,
        content=result.dict()
        )
        return response

    
    except Exception as e :
        return interanal_server_error_response(str(e))
  

async def get_follow_fans(current_user: Optional[dict] ,  
                            account_id : str ,
                            page : int ,
                        ) -> JSONResponse :
    try:
    
        member_id = current_user["account_id"] if current_user else None
        
        target_exist_result = db_check_target_exist_or_not(account_id)
        if target_exist_result is False:
            return data_not_found_error_response(DB_HAVE_NO_USER_DATA_ERROR)
        
        relation = db_check_member_target_relation(member_id , account_id)   
        if relation is False:
            return forbidden_error_response(USER_NOT_AUTHENTICATED_ERROR)
        
        
        result = db_get_follow_fans(member_id , account_id , page)
        response = JSONResponse(
        status_code = status.HTTP_200_OK,
        content=result.dict()
        )
        return response

    except Exception as e :
        return interanal_server_error_response(str(e))