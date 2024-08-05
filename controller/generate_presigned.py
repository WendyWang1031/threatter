import boto3
from fastapi import *
from model.model import *
from db.post_new import *

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
