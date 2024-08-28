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
    print("presignedUrl_request:",presignedUrl_request)
    return await generate_presigned_url(presignedUrl_request.file_name , presignedUrl_request.file_type)


@presigned_router.post("/api/post/process-and-upload-image",
        tags= ["Common"], 
        summary = "S3 重新處理影像",
         )
async def fetch_post_process_and_upload_image(
    background_tasks: BackgroundTasks,
    file_key: str = Body(...),
    file_type: str = Body(...)
    ) -> JSONResponse :
    if file_type.startswith("image/"):
        return await process_and_upload_image(file_key, file_type, background_tasks)
    elif file_type.startswith("video/"):
        return await process_and_upload_video(file_key, file_type, background_tasks)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
