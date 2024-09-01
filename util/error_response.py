import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from model.model_user import *


USER_NOT_AUTHENTICATED_ERROR = "User not authenticated"

DB_HAVE_NO_USER_DATA_ERROR = "No USER data have been found"
DB_HAVE_NO_POST_DATA_ERROR = "No POST data have been found"
DB_HAVE_NO_COMMENT_DATA_ERROR = "No COMMENT data have been found"
DB_HAVE_NO_NOTIFICATION_DATA_ERROR = "No Notification data have been found"

FAILED_REGISTER_USER_DATA_ERROR = "Email already exists"
FAILED_LOGIN_USER_DATA_ERROR = "Invalid email or password"

FAILED_UPDATE_DATA_ERROR = "FAILED to update data"
FAILED_DELETE_DATA_ERROR = "FAILED to delete data"
FAILED_DELETE_POST_DATA_ERROR = "FAILED to delete data or not your post id"
FAILED_UPDATE_FOLLOW_PRIVATE_DATA_ERROR = "Failed to insert private follower's data"

FAILED_GET_DATA_ERROR = "FAILED to get data"
FAILED_GET_POST_DATA_ERROR = "FAILED to get data"
FAILED_GET_MEMBER_POST_DATA_ERROR = "FAILED to get member's posts data"
FAILED_GET_COMMENT_DATA_ERROR = "FAILED to get comment data"
FAILED_GET_FOLLOW_DATA_ERROR = "User is already following the target user"

FAILED_UPDATE_USER_DATA_ERROR = "Failed to create user due to a server error"
FAILED_UPDATE_MEMBER_DATA_FIELD_EMPTY_ERROR = "At least one field must be updated"
FAILED_UPDATE_POST_DATA_FIELD_EMPTY_ERROR = "At least one field must be updated"
FAILED_UPDATE_COMMENT_DATA_FIELD_EMPTY_ERROR = "At least one field must be updated"
FAILED_UPDATE_REPLY_DATA_FIELD_EMPTY_ERROR = "At least one field must be updated"

def bad_request_error_response(message :str):
    error_response = ErrorResponse(error=True, message=message)
    response = JSONResponse (
        status_code=status.HTTP_400_BAD_REQUEST, 
        content=error_response.dict())
    return response

def forbidden_error_response(message :str):
    error_response = ErrorResponse(error=True, message=message)
    response = JSONResponse (
        status_code=status.HTTP_403_FORBIDDEN, 
        content=error_response.dict())
    return response

def data_not_found_error_response(message :str):
    error_response = ErrorResponse(error=True, message=message)
    response = JSONResponse (
        status_code=status.HTTP_404_NOT_FOUND, 
        content=error_response.dict())
    return response

def interanal_server_error_response(message :str):
    error_response = ErrorResponse(error=True, message=message)
    response = JSONResponse (
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        content=error_response.dict())
    return response

def successful_response():
    success = SuccessfulRes(success=True)
    response = JSONResponse(
    status_code = status.HTTP_200_OK,
    content=success.dict()
    )
    return response

def successful_response_register():
    success = SuccessfulResponseForRegister(success=True)
    response = JSONResponse(
    status_code = status.HTTP_200_OK,
    content=success.dict()
    )
    return response