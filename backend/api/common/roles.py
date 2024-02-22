from enum import Enum

from backend.api.common.route import MetaEnum


class Role(Enum, metaclass=MetaEnum):
    WEB_ADMIN = 'webadmin'
    SIMPLE_USER = 'simpleuser'
