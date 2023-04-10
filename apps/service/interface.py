from utils.reference import CACHE_CONFIGURE

from .models import Configure


async def get_configure(key):
    if not (value := CACHE_CONFIGURE.get(key)):
        if not (value := await Configure.filter(name=key, active=True).first()):
            return None
        CACHE_CONFIGURE[key] = value
    return value
