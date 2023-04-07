from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from utils.reference import Template

router = APIRouter(prefix="/service")


@router.get("/index", response_class=HTMLResponse)
async def service_index(request: Request):
    return Template.TemplateResponse(
        "base.html",
        {"request": request, "name": request.query_params.get("name")}
    )
