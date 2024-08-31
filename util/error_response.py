import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *


USER_NOT_AUTHENTICATED_ERROR = "User not authenticated"
USER_HAVE_NO_DATA_ERROR = "No data have been found"

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