from typing import Dict

from .models import Configure

GLOBAL_CONFIGURE: Dict[str, Configure] = {}


async def update_configure(**kwargs):
    if not kwargs:
        GLOBAL_CONFIGURE.clear()
        for configure in await Configure.filter(active=True):
            GLOBAL_CONFIGURE[configure.name] = configure
    else:
        instance = GLOBAL_CONFIGURE[kwargs["name"]]
        instance.value = str(kwargs["value"])
        await instance.save()
