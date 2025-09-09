import redis

from api.conf import settings


class RedisStorage:
    def __init__(self):
        self.__redis = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=0,
            ssl=settings.REDIS_SSL,
            ssl_certfile=settings.REDIS_SSL_CERTFILE,
            ssl_keyfile=settings.REDIS_SSLKEYFILE,
            ssl_ca_certs=settings.REDIS_SSL_CA_CERTS,
        )

    # def get_redis(self):
    #     return self.__redis

    def add(self, *args, **kwargs):
        return self.__redis.set(*args, **kwargs)

    def get(self, name):
        return self.__redis.get(name)

    def delete(self, *names):
        return self.__redis.delete(*names)

    def keys(self):
        return self.__redis.keys()

    def __del__(self):
        self.__redis.close()

    def remove_all(self):
        keys: list = self.__redis.keys()
        if keys:
            self.delete(*keys)
