import datetime

from api.common.redis_storage import RedisStorage
from api.conf.ldap import config as ldap_conf


class FreeIdGetter:

    def __init__(self, connection):
        self.reserved_identifiers = RedisStorage()
        self.connection = connection

    def have_greater_five_minute(self, timestamp_value):
        return datetime.datetime.fromtimestamp(int(timestamp_value)) + \
            datetime.timedelta(minutes=5) < datetime.datetime.now()

    def get_uid_numbers_from_ldap(self):
        self.connection.search(
            search_base=ldap_conf['LDAP_BASE_DN'],
            search_filter="(objectClass=Person)",
            attributes=["gidNumber"]
        )
        items = self.connection.response
        ids = []
        for item in items:
            ids.append(item["attributes"]["gidNumber"])

        return set(ids)

    def remove_all(self):
        self.reserved_identifiers.remove_all()

    def reserve(self, name):
        self.reserved_identifiers.add(
            name=name,
            value=int(datetime.datetime.now().timestamp())
        )

    def delete_from_reserved(self, name):
        if name:
            self.reserved_identifiers.delete(name)

    def get_free_spaces(self, ids):  # redis storage

        if not ids:
            return 10000

        sorted_ids = sorted(filter(lambda x: x >= 10000, ids))

        if not sorted_ids:
            return 10000

        for i in range(len(sorted_ids) - 1):
            count_free_spaces = sorted_ids[i + 1] - sorted_ids[i] - 1
            if count_free_spaces > 0:
                for number in range(sorted_ids[i] + 1, sorted_ids[i + 1]):
                    value = self.reserved_identifiers.get(number)
                    if value and self.have_greater_five_minute(value):
                        self.delete_from_reserved(number)
                        self.reserve(number)
                        return number

                    if not value:
                        self.reserve(number)
                        return number

        new_value = sorted_ids[-1] + 1
        while self.reserved_identifiers.get(new_value):
            new_value += 1

        self.reserve(new_value)
        return new_value
