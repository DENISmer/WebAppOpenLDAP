from backend.api.redis.redis_storage import RedisStorage


class GetFreeId:

    def __init__(self):
        self.reserved_identifiers = RedisStorage()

    def reserve(self, value):
        self.reserved_identifiers.add(name=value, value=f'{value}')

    def delete_from_reserved(self, value):
        if value:
            self.reserved_identifiers.delete(value)

    def get_free_spaces(self, ids):  # redis storage

        if not ids:
            return 10000

        sorted_ids = sorted(filter(lambda x: x >= 10000, ids))

        if not sorted_ids:
            return 10000

        j = 1
        for i in range(len(sorted_ids)-1):
            count_free_spaces = sorted_ids[i+1] - sorted_ids[i] - 1
            if count_free_spaces > 0:
                not_reserved_id = sorted_ids[i] + j

                if not self.reserved_identifiers.get(not_reserved_id):
                    self.reserve(not_reserved_id)
                    return not_reserved_id
                j += 1

        new_val = sorted_ids[-1] + 1
        while self.reserved_identifiers.get(new_val):
            new_val += 1

        self.reserve(new_val)
        return new_val
