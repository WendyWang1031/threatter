import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.follow import *
from db.check_relation import *
from db.get_member_data import *
from service.security import security_get_current_user


async def post_follow_target(follow : FollowReq , 
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

        # db get relation state
        # check relation state (None, Following)
        relation = db_check_each_other_relation(member_id , follow.account_id)
        if follow.follow is True and relation == "Following" :
            error_response = ErrorResponse(error=True, message="該用戶已追蹤對方")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response
       
       
        relation_state , insert_result = db_follow_target(follow , member_id)
        if insert_result is False:
            error_response = ErrorResponse(error=True, message="Failed to insert private follower's data")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response

        # db get FollowMember
        
        follow_member_data = db_get_member_single_data(follow.account_id, relation_state)
        if follow_member_data:
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=follow_member_data.dict()
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
    
async def post_private_user_res_follow(followAns : FollowAns ,
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
        
          
        # db get relation state
        # check relation state (Pending)
        relation = db_check_each_other_relation(member_id , followAns.account_id)
        
        if followAns.accept is True and relation == "Following" :
            error_response = ErrorResponse(error=True, message="該用戶已追蹤對方")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response
          
        # db change relation state
        relation_state , insert_result = db_private_user_res_follow(followAns , followAns.account_id , member_id)
        # check success or fail
        if insert_result is False:
            error_response = ErrorResponse(error=True, message="Failed to insert private follower's data")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response

        # db get FollowMember
        follow_member_data = db_get_member_single_data(followAns.account_id, relation_state)

        if follow_member_data:
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=follow_member_data.dict()
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
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response

async def get_follow_target(current_user: Optional[dict] ,  
                            account_id : str ,
                            page : int ,
                        ) -> JSONResponse :
    try:
    
        member_id = current_user["account_id"] if current_user else None

        target_exist_result = db_check_target_exist_or_not(account_id)
        # print("target_exist_result:",target_exist_result)
        if target_exist_result is False:
            error_response = ErrorResponse(error=True, message="資料庫並不存在該用戶資料")
            response = JSONResponse (
                status_code=status.HTTP_404_NOT_FOUND, 
                content=error_response.dict())
            return response
        
        
        relation = db_check_member_target_relation(member_id , account_id)  
        if relation is False:
            error_response = ErrorResponse(error=True, message="該用戶並無權限調閱")
            response = JSONResponse (
                status_code=status.HTTP_403_FORBIDDEN, 
                content=error_response.dict())
            return response
        
        
        result = db_get_follow_target(member_id , account_id , page)
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
  

async def get_follow_fans(current_user: Optional[dict] ,  
                            account_id : str ,
                            page : int ,
                        ) -> JSONResponse :
    try:
    
        member_id = current_user["account_id"] if current_user else None
        
        target_exist_result = db_check_target_exist_or_not(account_id)
        if target_exist_result is False:
            error_response = ErrorResponse(error=True, message="資料庫並不存在該用戶資料")
            response = JSONResponse (
                status_code=status.HTTP_404_NOT_FOUND, 
                content=error_response.dict())
            return response
        
        relation = db_check_member_target_relation(member_id , account_id)   
        if relation is False:
            error_response = ErrorResponse(error=True, message="該用戶並無權限調閱")
            response = JSONResponse (
                status_code=status.HTTP_403_FORBIDDEN, 
                content=error_response.dict())
            return response
        
        
        result = db_get_follow_fans(member_id , account_id , page)
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