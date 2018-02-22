import types
import sys
import logging

logger = logging.getLogger(__name__)

# Handlers
from . import handler_access_key_rotation
#...

## Master list of handlers
__handler_list = []

# Walk the globals list and return all modules...
def imports():
    for name, val in globals().copy().items():
        if isinstance(val, types.ModuleType):
            yield val.__name__


# ...and now ensure that they're the ones we're looking for
for x in imports():
    if "handlers.handler_" in x:
        logger.info('Found %s', x)
        cls = sys.modules[x].getClass()
        __handler_list.append(cls)


def get_all_handlers():
    return __handler_list
