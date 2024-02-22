from enum import Enum

from backend.api.common.route import MetaEnum


class Role(Enum, metaclass=MetaEnum):
    WEBADMIN = 'webadmins'
    SIMPLE_USER = 'simple_user'
