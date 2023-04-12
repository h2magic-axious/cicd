from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from utils.reference import Template

router = APIRouter(prefix="/service", default_response_class=HTMLResponse)


@router.get("/login")
async def service_login(request: Request):
    return Template.TemplateResponse("login.html", {"request": request})


@router.get("/index")
async def service_index(request: Request):
    return Template.TemplateResponse("services.html", {"request": request})


@router.get("/version/{name}")
async def service_version(request: Request, name: str):
    return Template.TemplateResponse("versions.html", {"request": request, "name": name})
