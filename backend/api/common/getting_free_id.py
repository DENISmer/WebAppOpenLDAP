
class GetFreeId:
    reserved_identifiers = []

    @classmethod
    def reserve(cls, value):
        cls.reserved_identifiers.append(value)

    @classmethod
    def del_from_reserved(cls, value):
        cls.reserved_identifiers.remove(value)

    def get_free_spaces(self, ids):

        if not ids:
            return 10000

        sorted_ids = sorted(filter(lambda x: x >= 10000, ids))

        j = 1
        for i in range(len(sorted_ids)-1):
            count_free_spaces = sorted_ids[i+1] - sorted_ids[i] - 1
            if count_free_spaces > 0:
                not_used_id = sorted_ids[i] + j
                if not_used_id not in self.reserved_identifiers:
                    self.reserve(not_used_id)
                    return not_used_id
                j += 1

        new_val = sorted_ids[-1] + 1
        while new_val in self.reserved_identifiers:
            new_val += 1

        self.reserve(new_val)
        return new_val
