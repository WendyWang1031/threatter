from fastapi import *
from fastapi.responses import FileResponse 
from controller.post import * 
from model.model import *
from fastapi.staticfiles import StaticFiles




app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# 會員頁面
@app.post("/api/post",
        tags= ["Post"],
        response_model = PostGetResponse , 
        summary = "修改會員資料",
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
async def fetch_post_post(content: str = Form(...) , image_url: UploadFile = File(...)) -> JSONResponse :
    post_data = PostDataRequest(content=content)
    return await update_post_data(post_data , image_url)

@app.get("/api/post",
        tags= ["Post"],
        response_model = PostGetResponse , 
        summary = "根據當前用戶取得會員資訊",
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
