import boto3
from model.model import *
from fastapi import *
from fastapi.responses import JSONResponse

from botocore.config import Config
from dotenv import load_dotenv
import os
# import subprocess
# import botocore.exceptions


load_dotenv()
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')  
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')  


def generate_presigned_post_to_s3(file_name: str, file_type: str):
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
    presigned_url, cdn_url = generate_presigned_post_to_s3(file_name , file_type)
    if presigned_url and cdn_url:
        return {"presigned_url": presigned_url, "cdn_url": cdn_url}
    else:
        raise HTTPException(status_code=500, detail="Failed to generate URLs")

# def process_image_with_imagemagick(input_path: str, output_path: str, width: int, height: int):
#     try:
#         command = f"magick convert {input_path} -resize {width}x{height} {output_path}"
#         subprocess.run(command, shell=True, check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"ImageMagick processing failed: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Image processing failed.")

# def process_video_with_ffmpeg(input_path: str, output_path: str):
#     try:
#         command = f"ffmpeg -i {input_path} -vcodec libx264 -crf 28 {output_path}"
#         subprocess.run(command, shell=True, check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"FFmpeg processing failed: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Video processing failed.")
    
# async def process_and_upload_image(file_key: str, 
#                                    file_type: str,
#                                    background_tasks: BackgroundTasks
#                                    ) -> JSONResponse:

#     download_path = f"/tmp/{file_key.split('/')[-1]}"
#     processed_path = f"/tmp/processed-{file_key.split('/')[-1]}"

#     s3_client = boto3.client('s3', 
#                              aws_access_key_id=aws_access_key_id, 
#                              aws_secret_access_key=aws_secret_access_key, 
#                              region_name='us-west-2')
    
#     try:
#         s3_client.download_file('threatter', file_key, download_path)
#     except botocore.exceptions.ClientError as e:
#         if e.response['Error']['Code'] == '404':
#             print("The file does not exist in S3.")
#             raise HTTPException(status_code=404, detail="File not found in S3.")
#         else:
#             raise

   
#     process_image_with_imagemagick(download_path, processed_path, 800, 600)

    
#     processed_file_key = f"processed_{file_key}"
#     with open(processed_path, "rb") as f:
#         s3_client.upload_fileobj(f, 'threatter', processed_file_key)


#     # 刪除本地臨時文件
#     background_tasks.add_task(os.remove, download_path)
#     background_tasks.add_task(os.remove, processed_path)
#     cdn_url_processed = f"https://d2z39jwxl0fy6f.cloudfront.net/{processed_file_key}"

#     return {"cdn_url": cdn_url_processed}

# async def process_and_upload_video(file_key: str, 
#                                    file_type: str,
#                                    background_tasks: BackgroundTasks
#                                    ) -> JSONResponse:

#     download_path = f"/tmp/{file_key.split('/')[-1]}"
#     processed_path = f"/tmp/processed-{file_key.split('/')[-1]}"

#     s3_client = boto3.client('s3', 
#                              aws_access_key_id=aws_access_key_id, 
#                              aws_secret_access_key=aws_secret_access_key, 
#                              region_name='us-west-2')
    
#     try:
#         s3_client.download_file('threatter', file_key, download_path)
#     except botocore.exceptions.ClientError as e:
#         if e.response['Error']['Code'] == '404':
#             print("The file does not exist in S3.")
#             raise HTTPException(status_code=404, detail="File not found in S3.")
#         else:
#             raise


#     process_video_with_ffmpeg(download_path, processed_path)

#     processed_file_key = f"processed_{file_key}"
#     with open(processed_path, "rb") as f:
#         s3_client.upload_fileobj(f, 'threatter', processed_file_key)


#     background_tasks.add_task(os.remove, download_path)
#     background_tasks.add_task(os.remove, processed_path)
#     cdn_url_processed = f"https://d2z39jwxl0fy6f.cloudfront.net/{processed_file_key}"

#     return {"cdn_url": cdn_url_processed}