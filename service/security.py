from jose import jwt , JOSEError
from datetime import datetime, timedelta 
from fastapi import  Security , HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv
import os
from fastapi import *
from model.model import *

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
security = HTTPBearer()

def security_create_access_token(data: dict , expires_delta: timedelta = timedelta(days = 7)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 60)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)
    return encoded_jwt

def security_decode_access_token(token: str):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=ALGORITHM)
        return payload
    
    except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403 , detail="Token 已過期")
    except JOSEError:
            raise HTTPException(status_code=403 , detail="Token 失效")
    
def security_get_current_user(token: HTTPAuthorizationCredentials = Security(security)) :
 
    user_info = security_decode_access_token(token.credentials)
    
    if not user_info:
            error_response = ServiceError(
                 error = True ,
                 status =  404 ,
                 error_code = "404-001" ,
                 error_message = "User not found")
            return None 
    else:
        return user_info