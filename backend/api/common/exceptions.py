
class UserIsNone(Exception):
    pass


class CouldNotCreateConnection(Exception):
    pass


class ItemFieldsIsNone(Exception):
    pass


def get_attribute_error_fields(fields: list, row: str) -> list:
    row = row.replace('\'', '')
    split_row = set(row.split(' '))
    keys = set(fields)
    out = (split_row & keys)
    return list(out)
