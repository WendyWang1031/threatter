from model.model import *
from fastapi.responses import JSONResponse
from starlette import status
import bcrypt

from db.user import *
from service.security import security_create_access_token 

async def register_user(user_request : UserRegisterReq) -> JSONResponse :
    
    try:
        check_exist = UserCheckExistReq(
            account_id = user_request.account_id , 
            email = user_request.email)
        if db_check_user_accountId_email_exists(check_exist) :
            error_response = ErrorResponse(error=True, message="Email already exists")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response

        # hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), bcrypt.gensalt())
        # user_request.password = hashed_password

        if db_insert_new_user(user_request) is True :
            success_response = SuccessfulResponseForRegister(success=True)
            response = JSONResponse(
                status_code=status.HTTP_200_OK,
                content=success_response.dict()
            )
            return response
        else:
            error_response = ErrorResponse(error=True, message="Failed to create user due to a server error")
            response = JSONResponse (
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                content=error_response.dict())
            return response
    
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response
    
async def authenticate_user(user_login_req : UserPutReq) -> JSONResponse :
    
    try:
        user_info = db_check_accountId_password(user_login_req)
        
        if user_info:
            access_token = security_create_access_token(UserGetCheck(
                name = user_info['name'],
                account_id = user_info['account_id']
            ).dict())
            success_response = Token(token = access_token)
            response = JSONResponse(
                status_code=status.HTTP_200_OK,
                content=success_response.dict()
            )
            return response
        
        else:
            error_response = ErrorResponse(error=True, message="Invalid email or password")
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
    
async def get_user_details(user: UserGetCheck) -> JSONResponse :
    try:
        if not user :
            error_response = ErrorResponse(error=True, message="Failed to get user's data")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response
            
        user_model = UserGetCheck(**user)

        if user["account_id"] is None :
            error_response = ErrorResponse(error=True, message="User not found")
            response = JSONResponse (
            status_code=status.HTTP_404,
            content=user_model.dict()
        )           
            return response
        
        else:    
            response = JSONResponse (
                status_code=status.HTTP_200_OK,
                content= user_model.dict()
            )           
            return response

    except KeyError :
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