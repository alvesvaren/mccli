
from typing import Any, Callable, Dict, List, Text, TextIO, Union
import json
import re
_loaddict = Dict[str, Union[str, int, float, bool]]
_types = {
    "true": True,
    "false": False,
    "null": None
}


def cast_if_possible(func: Callable, value: Any) -> Any:
    try:
        value = func(value)
    except ValueError:
        pass
    return value


def load(file: TextIO) -> _loaddict:
    return loads(file.read())


def loads(string: str) -> _loaddict:
    output: _loaddict = {}
    for line in string.splitlines():
        key, value = line.strip().split("=")
        if re.match(r"\d+", value):
            value = cast_if_possible(int, value)
        elif re.match(r"\d+\.\d+", value):
            value = cast_if_possible(float, value)

        if (value in _types.keys()):
            value = _types[value]

        output[key] = value
    return output


def dump(obj: _loaddict, fp: TextIO) -> None:

    dumps(obj)


def dumps(obj: _loaddict) -> str:
    output: str = ""
    for key, value in obj.items():
        try:
            value = list(_types.keys())[list(_types.values()).index(value)]
        except ValueError:
            pass
        output += f"{key}={value}\n"
    return output
