import re

class UserIsNone(Exception):
    pass


class CouldNotCreateConnection(Exception):
    pass


class ItemFieldsIsNone(Exception):
    pass


def get_attribute_error_message(fields: list, row: str) -> list:
    return list(set(re.findall("|".join(fields), row)))


def form_dict_field_error(object_item, message):
    return {
        item: [message]
        for item in get_attribute_error_message(
            list(object_item.fields.keys()), message
        )
    }
