from apps.service.models import Service
from utils.environments import Env
from utils.settings import BASE_DIR
from utils.reference import execute

DATA_DIR = BASE_DIR.joinpath("data")


class ServiceAgent:
    __instance_map = dict()
    registry = Env.REGISTRY
    network = Env.NETWORK

    def __new__(cls, service: Service):
        if service.name not in cls.__instance_map:
            cls.__instance_map[service.name] = object.__new__(cls)
        return cls.__instance_map[service.name]

    def __init__(self, service: Service):
        self.service = service

    def mark_tag(self, version):
        if self.registry is None:
            return f"{self.service.name}:{version}"
        else:
            return f"{self.registry}/{self.service.name}:{version}"

    async def git_clone(self):
        p = DATA_DIR.joinpath(self.service.name)

        if p.exists():
            execute(f"git -C {p} pull")
        else:
            execute(f"git clone {self.service.repository} {p}")

        return str(p)

    async def build(self, version):
        p = await self.git_clone()
        image_tag = self.mark_tag(version)
        execute(f"docker build -f {p}/Dockerfile -t {image_tag} {p}")
        execute(f"docker push {image_tag}")

    async def run(self, version):
        execute(f"docker stop {self.service.name}")
        execute(f"docker rm {self.service.name}")
        execute(f"docker run -d --name {self.service.name} --{self.network} {self.mark_tag(version)}")
