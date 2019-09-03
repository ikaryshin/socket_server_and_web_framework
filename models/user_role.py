import json
from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()

    def translate(self, _escape_table):
        return self.name


class JSONEncoder(json.JSONEncoder):
    prefix = "__enum__"

    def default(self, o):
        if isinstance(o, UserRole):
            return {self.prefix: o.name}
        else:
            return super().default(o)


def json_decode(d):
    if JSONEncoder.prefix in d:
        name = d[JSONEncoder.prefix]
        return UserRole[name]
    else:
        return d
