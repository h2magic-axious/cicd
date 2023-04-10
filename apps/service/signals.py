from tortoise.signals import post_save

from utils.reference import CACHE_CONFIGURE
from .models import Configure


@post_save(Configure)
async def update_cache_configure_after_configure_updated(*args):
    instance: Configure = args[1]
    CACHE_CONFIGURE[instance.name] = instance.value
