from collections import defaultdict

from service.models import ContainerConfigure, Service

from utils.git_docker import CACHE_SERVICE


async def build_run_configure(service: Service):
    if service.name not in CACHE_SERVICE:
        temp = defaultdict(dict)

        for configure in await ContainerConfigure.filter(service=service, active=True):
            match configure.configure_type:
                case ContainerConfigure.CType.PORT.value:
                    c_type = "ports"
                case ContainerConfigure.CType.VOLUME.value:
                    c_type = "volumes"
                case _:
                    c_type = "environment"

            temp[c_type][configure.c_left] = configure.c_right

        CACHE_SERVICE[service.name] = temp

    return {
        "ports": {f"{left}/tcp": right for left, right in CACHE_SERVICE[service.name]["ports"].items()},
        "environment": CACHE_SERVICE[service.name]["environment"],
        "volumes": {
            left: {"bind": right, "mode": "rw"} for left, right in CACHE_SERVICE[service.name]["volumes"].items()
        }
    }
