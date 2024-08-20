from fastapi import *
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse ,RedirectResponse

##
from service.router_search import search_router
from service.router_user import user_router
from service.router_member import member_router
from service.router_post import post_router
from service.router_follow import follow_router
from service.router_comment import comment_router
from service.router_presigned_url import presigned_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)
app.include_router(member_router)
app.include_router(search_router)
app.include_router(post_router)
app.include_router(follow_router)
app.include_router(comment_router)
app.include_router(presigned_router)

# ----------------------------------------------------------

# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
    return FileResponse("./static/index.html", media_type="text/html")

@app.get("/member/{account_id}", include_in_schema=False)
async def member(request: Request):
    return FileResponse("./static/member.html", media_type="text/html")

@app.get("/member/{account_id}/post/{post_id}", include_in_schema=False)
async def member_single_post(request: Request):
    return FileResponse("./static/single_page.html", media_type="text/html")

@app.get("/notification", include_in_schema=False)
async def notification(request: Request):
    return FileResponse("./static/notification.html", media_type="text/html")

@app.get("/search", include_in_schema=False)
async def search(request: Request):
    return FileResponse("./static/search.html", media_type="text/html")


@app.get("/member")
async def redirect_to_home(request: Request):
    return RedirectResponse(url="/")
 