from strpipe.data.types import (
    STRING,
    STRING_LIST,
    INT_LIST,
)


def _infer_type(content):
    return STRING


class Datum:
    """For ops to consume and produce."""

    def __init__(self, content):
        self.content = content
        self.type = _infer_type(content)
