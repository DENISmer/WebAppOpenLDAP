import re


def validate_str(value) -> bool:
    regex = '^\w+$'
    pattern = re.compile(regex)

    if pattern.search(value) is None:
        return False

    return True
