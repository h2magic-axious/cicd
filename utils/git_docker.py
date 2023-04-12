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
    image, build_logs = DockerClient.images.build(path=p, tag=tag(service, version))

    for log in build_logs:
        if "stream" in log:
            print(log["stream"], end="")

    return image.id.split(":")[-1]


def docker_stop(service: Service):
    if container := DockerClient.containers.get(service.container_id):
        container.remove()


def docker_rmi(image_id):
    DockerClient.images.remove(image_id)


def docker_tag(old_tag, new_tag):
    DockerClient.api.tag(old_tag, new_tag)
    DockerClient.images.remove(old_tag)


def docker_run(service: Service, version):
    docker_stop(service)

    container = DockerClient.containers.run(
        image=tag(service, version), name=service.name, network=Env.NETWORK, detach=True
    )

    return container.id
