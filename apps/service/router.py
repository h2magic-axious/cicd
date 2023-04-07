from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from utils.reference import Template

router = APIRouter(prefix="/service")


@router.get("/login", response_class=HTMLResponse)
async def service_login(request: Request):
    return Template.TemplateResponse(
        "login.html",
        {"request": request}
    )


@router.get("/index", response_class=HTMLResponse)
async def service_index(request: Request):
    return Template.TemplateResponse(
        "index.html",
        {"request": request}
    )
