from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from apps.service.models import Service, History
from utils.git_docker import docker_build, docker_run, docker_rmi, docker_stop, docker_tag, tag
from utils.reference import Template, response_result

router = APIRouter(prefix="/service")


@router.get("/login", response_class=HTMLResponse)
async def service_login(request: Request):
    return Template.TemplateResponse("login.html", {"request": request})


@router.get("/index", response_class=HTMLResponse)
async def service_index(request: Request):
    return Template.TemplateResponse("services.html", {"request": request})


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


@router.post("/api/api-change-version")
async def api_change_version(request: Request):
    body = await request.json()
    if not (history := await History.filter(id=body["id"]).first()):
        return response_result(0, "Version not found")

    if body["field"] == "version":
        if body["value"] == history.version:
            return response_result(1, "success")
        
        service = await history.service
        try:
            docker_tag(tag(service, history.version), tag(service, body["value"]))
            history.version = body["value"]
        except Exception as e:
            return response_result(0, str(e))
    else:
        history.description = body["value"]

    await history.save()
    return response_result(1, "success")


@router.get("/version/{name}", response_class=HTMLResponse)
async def service_version(request: Request, name: str):
    return Template.TemplateResponse("versions.html", {"request": request, "name": name})


@router.get("/api-versions/{name}")
async def api_versions(name: str):
    return response_result(
        1,
        [
            {
                "id": history.image_id[:12],
                "created_at": history.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "version": history.version,
                "description": history.description,
                "running": history.running,
            }
            for history in await History.filter(service__name=name).order_by("-created_at")
        ],
    )


@router.post("/api-new-service")
async def new_service(request: Request):
    body = await request.json()
    if await Service.filter(name=body["name"]).exists():
        return response_result(0, "Service already exists")

    await Service.create(**body)
    return response_result(1, "success")


@router.get("/api-delete/{pk}")
async def delete_version_history(pk):
    if history := await History.filter(image_id__contains=pk).first():
        if history.running:
            docker_stop(await history.service)
        else:
            docker_rmi(history.image_id)

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
        await History.create(
            service=service, 
            version=body["version"], 
            description=body["description"],
            image_id=docker_build(service, body["version"])
        )
    except Exception as e:
        return response_result(0, str(e))

   
    return response_result(1, "success")


@router.get("/api-run/{history_id}")
async def run_history(history_id):
    if not (history := await History.filter(image_id__contains=history_id).first()):
        return response_result(0, "Version not found")
    
    service: Service = await history.service

    if (old_version := await History.filter(service=service, running=True).first()):
        old_version.running = False
        await old_version.save()

    service.container_id = docker_run(service, history.version)
    history.running = True

    print(service.name, service.container_id)
    await history.save()
    await service.save()

    return response_result(1, "success")
