from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from apps.service.models import Configure, Service
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
        "services.html",
        {"request": request}
    )


@router.get("/settings", response_class=HTMLResponse)
async def service_settings(request: Request):
    return Template.TemplateResponse(
        "settings.html",
        {"request": request}
    )


@router.get("/api-settings")
async def api_settings():
    return response_result(1, await Configure.all())


@router.post("/api-change-setting")
async def api_change_setting(request: Request):
    body = await request.json()
    if not (configure := await Configure.filter(name=body["name"]).first()):
        return response_result(0, f"Configure({body['name']}) not found")

    if body["field"] == "active":
        configure.active = body["value"]
    else:
        configure.value = str(body["value"])

    await configure.save()
    return response_result(1, "success")


@router.get("/api-services")
async def api_services():
    return response_result(1, await Service.all())


@router.post("/api-change-service")
async def api_change_service(request: Request):
    body = await request.json()
    if not (service := await Service.filter(id=body["id"]).first()):
        return response_result(0, "Service not found")

    await service.update_from_dict({body["field"]: body["value"]})
    await service.save()
    return response_result(1, "success")
