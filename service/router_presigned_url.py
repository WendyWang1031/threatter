from fastapi import APIRouter
from model.model import *
from model.model_user import *

from controller.presigned_url import * 

from fastapi.responses import JSONResponse

presigned_router = APIRouter()

# 共用
@presigned_router.post("/api/post/generate-presigned-url",
        tags= ["Common"], 
        summary = "S3 產生欲簽名 URL",
         )
async def fetch_post_generate_presigned_url(presignedUrl_request: PresignedUrlRequest) -> JSONResponse :
    return await generate_presigned_url(presignedUrl_request.file_name , presignedUrl_request.file_type)
