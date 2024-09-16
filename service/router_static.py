from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, RedirectResponse


static_router = APIRouter()
# Static Pages (Never Modify Code in this Block)
@static_router.get("/", include_in_schema=False)
async def index(request: Request):
    return FileResponse("./static/index.html", media_type="text/html")

@static_router.get("/member/{account_id}", include_in_schema=False)
async def member(request: Request):
    return FileResponse("./static/member.html", media_type="text/html")

@static_router.get("/member/{account_id}/post/{post_id}", include_in_schema=False)
async def member_single_post(request: Request):
    return FileResponse("./static/single_page.html", media_type="text/html")

@static_router.get("/notification", include_in_schema=False)
async def notification(request: Request):
    return FileResponse("./static/notification.html", media_type="text/html")

@static_router.get("/search", include_in_schema=False)
async def search(request: Request):
    return FileResponse("./static/search.html", media_type="text/html")


@static_router.get("/member")
async def redirect_to_home(request: Request):
    return RedirectResponse(url="/")
 