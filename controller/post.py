import boto3
from model.model import *
from db.post import *

from fastapi import *
from fastapi.responses import JSONResponse



def upload_file_to_s3(file: UploadFile):
    s3_client = boto3.client('s3')
    bucket_name = "threatter"

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_extension = file.filename.split('.')[-1]
    file_key = f"test_post/{timestamp}-test_post.{file_extension}"
    
    content_type = file.content_type
    
    try:
        s3_client.upload_fileobj(
            file.file,
            bucket_name,
            file_key,
            ExtraArgs={
                'ContentType': content_type  
            }
        )
        return f"https://d2z39jwxl0fy6f.cloudfront.net/{file_key}"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def create_post_data(
        content: str = Form(default = None) ,
        image_url: UploadFile = File(default = None) ) -> JSONResponse :
    try:
        print("content1:",content)
        # 檢查圖片與文件是否已上傳
        if image_url and image_url.filename :
            result_image_url = upload_file_to_s3(image_url)
            if not result_image_url:
                error_response = ErrorResponse(error=True, message="圖片上傳失敗")
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    content=error_response.dict())
        else:
            result_image_url = None 

        if not content and not image_url.filename:
            error_response = ErrorResponse(error=True, message="請至少要提供文字或圖片")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response

        content = content if content else "" 
        post_data_instance = PostData(content=content, image_url=result_image_url)
        result = db_update_post_data(post_data_instance)
        
        if result is True:
            success_response = PostGetResponse(ok=True, data=[post_data_instance])
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
    
    
async def get_post_data() -> JSONResponse :
    try:
        post_data =  db_get_post_data()
        
        if post_data :
            success_response = PostGetResponse(ok=True, data=post_data)
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=success_response.dict()
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