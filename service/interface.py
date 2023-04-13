from service.models import ContainerConfigure, Service

from utils.git_docker import CACHE_SERVICE


async def build_run_configure(service: Service):
    if service.name not in CACHE_SERVICE:
        CACHE_SERVICE[service.name] = {"ports": dict(), "environment": dict(), "volumes": dict()}

        for configure in await ContainerConfigure.filter(service=service, active=True):
            match configure.configure_type:
                case ContainerConfigure.CType.PORT.value:
                    ...
