import docker
import git

from apps.service.models import Service
from utils.environments import Env

from utils.settings import BASE_DIR

DATA_DIR = BASE_DIR.joinpath("data")


class ServiceAgent:
    __instance_map = dict()
    registry = Env.REGISTRY
    client = docker.from_env() if Env.DOCKER_SOCK else docker.DockerClient(base_url=Env.DOCKER_SOCK)
    network = Env.NETWORK

    def __new__(cls, service: Service):
        if service.name not in cls.__instance_map:
            cls.__instance_map[service.name] = object.__new__(cls)
        return cls.__instance_map[service.name]

    def __init__(self, service: Service):
        self.service = service

    def __del__(self):
        self.client.close()

    def mark_tag(self, version):
        if self.registry is None:
            return f"{self.service.name}:{version}"
        else:
            return f"{self.registry}/{self.service.name}:{version}"

    async def git_clone(self):
        p = DATA_DIR.joinpath(self.service.name)
        if p.exists():
            git.Repo(p).remote(name="origin").pull()
        else:
            git.Repo.clone_from(self.service.repository, p)

    async def build(self, version):
        await self.git_clone()

        response = self.client.api.build(
            path=str(DATA_DIR.joinpath(self.service.name)),
            dockerfile="Dockerfile",
            tag=self.mark_tag(version),
            rm=True,
            decode=True,
            pull=True
        )
        for line in response:
            print(line)
            if "aux" in line:
                temp: str = line["aux"]["ID"]
                return temp.split(":")[1]

    async def run(self, version):
        if container := self.client.containers.get(self.service.container_id):
            container.remove()

        container = self.client.containers.run(
            image=self.mark_tag(version),
            name=self.service.name,
            network=self.network,
            detach=True
        )
        self.service.container_id = container.id
        await self.service.save()
