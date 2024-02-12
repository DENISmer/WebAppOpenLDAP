import redis

from backend.api.redis import settings


class RedisStorage:
    def __init__(self):
        self.__redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            username=settings.REDIS_USERNAME,
            password=settings.REDIS_PASSWORD,
            ssl=settings.REDIS_SSL,
            ssl_certfile=settings.REDIS_SSL_CERTFILE,
            ssl_keyfile=settings.REDIS_SSLKEYFILE,
            ssl_ca_certs=settings.REDIS_SSL_CA_CERTS,
        )

    def get_redit(self):
        return self.__redis

    def add(self, *args, **kwargs):
        return self.__redis.set(*args, **kwargs)

    def get(self, name):
        return self.__redis.get(name)

    def delete(self, *names):
        return self.__redis.delete(*names)
