import re


class UserIsNone(Exception):
    pass


class CouldNotCreateConnection(Exception):
    pass


class ItemFieldsIsNone(Exception):
    pass


class InputFieldKeysIsNone(Exception):
    pass


class NotModifyItemIsNone(Exception):
    pass


class RouteIsNotDefine(Exception):
    pass


# def get_attribute_error_message(fields: list, row: str) -> list:
#     return list(set(re.findall("|".join(fields), row)))


def get_attribute_error_message(fields: list, row: str) -> list:
    row = re.sub(
        r'[:\'\";\\/]',
        lambda match: {'\'': '', '\"': '', ';': '', ':': '', '/': ''}.get(match.group(0)),
        row
    )
    split_row = set(row.split(' '))
    keys = set(fields)
    out = (split_row & keys)
    return list(out)


def form_dict_field_error(object_item, message):
    return {
        item: [message]
        for item in get_attribute_error_message(
            list(object_item.fields.keys()), message
        )
    }
