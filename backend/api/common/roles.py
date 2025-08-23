from enum import Enum, EnumMeta


class MetaEnum(EnumMeta):
    def __call__(cls, *args, **kwargs):
        names = kwargs.get('names')
        if names is not None:
            return super().__call__(*args, **kwargs)

        try:
            return super().__call__(*args, **kwargs)
        except ValueError:
            return None


class Role(Enum, metaclass=MetaEnum):
    WEB_ADMINS = 'webadmins'
    SIMPLE_USER = 'simpleuser'
