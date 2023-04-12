import docker
from git import Repo

from apps.service.models import Service
from utils.environments import Env
from utils.settings import BASE_DIR

DATA_DIR = BASE_DIR.joinpath("data")

DockerClient = docker.from_env()


def tag(service: Service, version):
    result = f"{service.name}:{version}"
    if Env.REGISTRY is not None:
        result = f"{Env.REGISTRY}/{result}"

    return result


def git_pull(service: Service):
    p = DATA_DIR.joinpath(service.name)

    if p.exists():
        Repo(p).remote(name="origin").pull()
    else:
        Repo.clone_from(service.repository, p)

    return str(p)


def docker_build(service: Service, version):
    p = git_pull(service)
    response = DockerClient.api.build(
        path=p,
        dockerfile="Dockerfile",
        tag=tag(service, version),
        rm=True,
        decode=True,
        pull=True,
    )
    for line in response:
        print(line)
        if "aux" in line:
            temp: str = line["aux"]["ID"]
            return temp.split(":")[1]


def docker_stop(service: Service):
    if container := DockerClient.containers.get(service.container_id):
        container.remove()


def docker_remove_container(container_id):
    DockerClient.images.remove(container_id)


def docker_run(service: Service, version):
    docker_stop(service)

    container = DockerClient.containers.run(
        image=tag(service, version), name=service.name, network=Env.NETWORK, detach=True
    )

    return container.id
