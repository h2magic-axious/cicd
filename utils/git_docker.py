import docker
from git import Repo

from service.models import Service
from utils.reference import try_to_do
from utils.environments import Env
from utils.settings import BASE_DIR

DATA_DIR = BASE_DIR.joinpath("data")

DockerClient = docker.from_env()

CACHE_SERVICE = dict()


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


@try_to_do
def docker_stop(service: Service):
    if service.container_id is None:
        return
    print("Container Id: ", service.container_id)
    if container := DockerClient.containers.get(service.container_id):
        container.stop()
        container.remove()


@try_to_do
def docker_rmi(image_id):
    DockerClient.images.remove(image_id)


@try_to_do
def docker_tag(old_tag, new_tag):
    DockerClient.api.tag(old_tag, new_tag)
    DockerClient.images.remove(old_tag)


def docker_run(service: Service, version, **kwargs):
    docker_stop(service)

    container = DockerClient.containers.run(
        image=tag(service, version), name=service.name, network=Env.NETWORK, detach=True, **kwargs
    )

    print("容器ID: ", container.id)

    return container.id
