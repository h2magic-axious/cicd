from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from apps.service.models import Service, History
from utils.git_docker import ServiceAgent
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


@router.get("/version/{name}", response_class=HTMLResponse)
async def service_version(request: Request, name: str):
    return Template.TemplateResponse(
        "versions.html",
        {"request": request, "name": name}
    )


@router.get("/api-versions/{name}")
async def api_versions(name: str):
    return response_result(1, [
        {
            "id": history.id,
            "image_id": history.image_id[:12],
            "created_at": history.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "version": history.version,
            "running": history.running
        } for history in await History.filter(service__name=name).order_by("-created_at")
    ])


@router.get("/api-delete/{pk}")
async def delete_version_history(pk):
    if history := await History.filter(id=pk).first():
        agent = ServiceAgent(await history.service)
        #
        if container := agent.client.containers.get(history.service.container_id):
            container.remove()

        agent.client.images.remove(history.image_id)

        await history.delete()

    return response_result(1, "success")


@router.post("/api-new-version")
async def service_new_version(request: Request):
    body = await request.json()
    if not (service := await Service.filter(name=body["name"]).first()):
        return response_result(0, "Service not found")

    if await History.filter(service=service, version=body["version"]).exists():
        return response_result(0, "Version has been existed")

    try:
        image_id = await ServiceAgent(service).build(body["version"])
    except Exception as e:
        return response_result(0, str(e))

    await History.create(service=service, version=body["version"], image_id=image_id)
    return response_result(1, "success")


@router.get("/api-run/{history_id}")
async def run_history(history_id):
    if not (history := await History.filter(id=history_id).first()):
        return response_result(0, "Version not found")

    service = await history.service
    old_version = await History.filter(service=service, running=True).first()

    if old_version:
        old_version.running = False
        await old_version.save()

    await ServiceAgent(service).run(history.version)
    return response_result(1, "success")
