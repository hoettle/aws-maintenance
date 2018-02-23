import types
import sys
import logging

import boto3
from boto3 import session

logger = logging.getLogger(__name__)

# Handlers
from . import handler_access_key_rotation
from . import handler_update_security_group
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
        handler = cls()
        __handler_list.append(handler)


def get_all_handlers():
    return __handler_list


class DummyHandler:
    def handle(self, my_session):
        sts = my_session.client('sts')
        ident = sts.get_caller_identity()
        print('Profile: {}, Account: {}, User:{}'.format(my_session.profile_name,ident['Account'], ident['Arn']))
