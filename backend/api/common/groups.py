from enum import Enum

from backend.api.common.route import MetaEnum


class Group(Enum, metaclass=MetaEnum):
    MEMBEROF = 'memberof'
    POSIXGROUP = 'posixgroup'
