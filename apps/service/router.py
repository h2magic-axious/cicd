from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from tortoise.expressions import Q

from apps.service.models import Configure
from utils.reference import Template, response_result

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


@router.get("/settings", response_class=HTMLResponse)
async def service_settings(request: Request):
    q = Q()
    if active := request.query_params.get("active"):
        q &= Q(active=(active == "yes"))

    return Template.TemplateResponse(
        "settings.html",
        {"request": request, "data": await Configure.filter(q)}
    )
