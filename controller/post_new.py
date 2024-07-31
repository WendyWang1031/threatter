import boto3
import json
from fastapi import *
from fastapi.responses import JSONResponse
from model.model import *
from db.post_new import *
from service.security import security_get_current_user

from botocore.config import Config
from dotenv import load_dotenv
import os

load_dotenv()
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')  
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')  


def generate_presigned_to_s3(file_name: str, file_type: str):
    print("file_type:" , file_type)

    s3_client = boto3.client('s3',
                aws_access_key_id = aws_access_key_id,
                aws_secret_access_key = aws_secret_access_key,
                region_name='us-west-2',
                config=Config(signature_version='s3v4')
            )
    bucket_name = "threatter"

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_extension = file_name.split('.')[-1]
    file_key = f"test_post/{timestamp}-test_post.{file_extension}"
    
    try:
        # 使用POST方法，前端部分尚未成功
        # presigned_url =  s3_client.generate_presigned_post(
        #     Bucket=bucket_name,
        #     Key=file_key,
        #     Fields={"acl": "public-read", "Content-Type": file_type},
        #     Conditions=[
        #         {"acl": "public-read"},
        #         {"Content-Type": file_type}
        #     ],
        #     ExpiresIn=3600
        # )
        

        presigned_url =  s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket_name, 
                    'Key': file_key },
            ExpiresIn=3600)
     
        
        cdn_url = f"https://d2z39jwxl0fy6f.cloudfront.net/{file_key}"
        
        return presigned_url , cdn_url
    
    except Exception as e:
        print(f"Failed to generate presigned URL: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def generate_presigned_url(file_name: str , file_type: str):
    presigned_url, cdn_url = generate_presigned_to_s3(file_name , file_type)
    if presigned_url and cdn_url:
        return {"presigned_url": presigned_url, "cdn_url": cdn_url}
    else:
        raise HTTPException(status_code=500, detail="Failed to generate URLs")


async def create_post_data(post_data : PostCreateReq , current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    try:
        if not current_user :
            error_response = ErrorResponse(error=True, message="User not authenticated")
            response = JSONResponse (
                    status_code=status.HTTP_403_FORBIDDEN, 
                    content=error_response.dict())
            return response

        if not post_data.content.text and not (post_data.content.media and (post_data.content.media.images or post_data.content.media.videos or post_data.content.media.audios)):
            error_response = ErrorResponse(error=True, message="請至少要提供文字或圖片")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response

        member_id = current_user["account_id"]    
        result = db_create_post_data(post_data , member_id)
        
        if result is True:
            success_response = SuccessfulRes(success=True)
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=success_response.dict()
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
    
    
async def get_post_home(current_user: Optional[dict], page: int) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        post_data = db_get_home_post_data(member_id , page)
        
        if post_data :
            
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=json.loads(post_data.json())
            )
            return response
            
        else:
            error_response = ErrorResponse(error=True, message="No post Data details found for user")
            response = JSONResponse (
                status_code=status.HTTP_404_NOT_FOUND, 
                content=error_response.dict())
            return response

        
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response
    
async def delete_post(post_id : str ,current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    try:
        if current_user :
            member_id = current_user["account_id"]
            delete_post_result = db_delete_post(post_id , member_id)
            
            if delete_post_result:
                success_response = SuccessfulRes(success=True)
                response = JSONResponse(
                status_code = status.HTTP_200_OK,
                content=success_response.dict()
                )
                return response
            else:
                response = JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": True,
                        "message": str(e)
                    })
                return response
        else:
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


async def get_post_member_page(current_user: Optional[dict], account_id: str , page: int) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        post_data = db_get_member_post_data(member_id , account_id , page)
        
        if post_data :
            
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=json.loads(post_data.json())
            )
            return response
            
        else:
            error_response = ErrorResponse(error=True, message="No member's post data details found for user")
            response = JSONResponse (
                status_code=status.HTTP_404_NOT_FOUND, 
                content=error_response.dict())
            return response

        
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response
  

async def get_post_single_page(current_user: Optional[dict], account_id: str , post_id : str) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
        post_data = db_get_single_post_data(member_id , account_id , post_id)
        
        if post_data :
            
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=json.loads(post_data.json())
            )
            return response
            
        else:
            error_response = ErrorResponse(error=True, message="No member's post data details found for user")
            response = JSONResponse (
                status_code=status.HTTP_404_NOT_FOUND, 
                content=error_response.dict())
            return response

        
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response
