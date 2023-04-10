import docker
import git

from apps.service.interface import get_configure
from apps.service.models import Service

from utils.settings import BASE_DIR

DATA_DIR = BASE_DIR.joinpath("data")


async def init_or_clone(git_path, to_path):
    p = DATA_DIR.joinpath(to_path)
    if p.exists():
        repo = git.Repo(p)
        origin = repo.remote(name="origin")
        origin.pull()
    else:
        repo = git.Repo.clone_from(git_path, p)

    return repo


async def build_image(dockerfile_path, container_name, version):
    registry = await get_configure("docker_registry")
    name = f"{registry}/{container_name}:{version}"

    client = docker.from_env()
    client.images.build(path=dockerfile_path, tag=name, rm=True)
    client.images.push(name)
    client.close()


async def deploy(service: Service, version, **kwargs):
    client = docker.from_env()
    registry = await get_configure("docker_registry")
    network = await get_configure("docker_network")

    if container := client.containers.get(service.container_id):
        container.remove()

    container = client.containers.run(
        image=f"{registry}/{service.container_name}:{version}",
        name=service.container_name,
        network=network,
        detach=True,
        **kwargs
    )

    service.container_id = container.id
    await service.save()

    client.close()
