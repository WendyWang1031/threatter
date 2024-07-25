from fastapi import *
from fastapi.responses import FileResponse 
from controller.post import * 
from model.model import *
from fastapi.staticfiles import StaticFiles




app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# 貼文頁面
@app.post("/api/post/generate-presigned-url",
        tags= ["Post"], 
        summary = "S3 產生欲簽名 URL",
         )
async def fetch_post_generate_presigned_url(presignedUrl_request: PresignedUrlRequest) -> JSONResponse :
    print("presignedUrl_request:", presignedUrl_request)
    return await generate_presigned_url(presignedUrl_request.file_name , presignedUrl_request.file_type)

@app.post("/api/post",
        tags= ["Post"],
        response_model = PostGetResponse , 
        summary = "新增貼文資料",
        responses = {
            200:{
                "model" : PostGetResponse,
                "description" : "修改成功"
            },
            400:{
                "model" : ErrorResponse,
                "description" : "修改失敗，輸入不正確或其他原因"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         }
         )
async def fetch_post_post(post_data : PostData) -> JSONResponse :
    print("post_data:",post_data)
    return await create_post_data(post_data)

@app.get("/api/post",
        tags= ["Post"],
        response_model = PostGetResponse , 
        summary = "根據id取得貼文資訊",
        responses = {
            200:{
                "model" : PostGetResponse,
                "description" : "成功取得貼文資料"
            },
            500:{
                "model" : ErrorResponse,
                "description" : "伺服器內部錯誤"
            }
         })
async def fetch_get_post() -> JSONResponse :
    return await get_post_data()

# ----------------------------------------------------------


# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
    return FileResponse("./static/index.html", media_type="text/html")
