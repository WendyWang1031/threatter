import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *


USER_NOT_AUTHENTICATED_ERROR = "User not authenticated"

DB_HAVE_NO_USER_DATA_ERROR = "No USER data have been found"
DB_HAVE_NO_POST_DATA_ERROR = "No POST data have been found"
DB_HAVE_NO_COMMENT_DATA_ERROR = "No COMMENT data have been found"
DB_HAVE_NO_NOTIFICATION_DATA_ERROR = "No Notification data have been found"

FAILED_UPDATE_DATA_ERROR = "FAILED to update data"
FAILED_GET_DATA_ERROR = "FAILED to get data"


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