
from typing import Any, Callable, Dict, TextIO, Union
import re
LoadDict = Dict[str, Union[str, int, float, bool]]
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


def load(file: TextIO) -> LoadDict:
    return loads(file.read())


def loads(string: str) -> LoadDict:
    output: LoadDict = {}
    for line in string.splitlines():
        if line.startswith("#"):
            key, value = "#", line[1:]
        else:
            key, value = line.strip().split("=")
        if re.match(r"^\d+$", value):
            value = cast_if_possible(int, value)
        elif re.match(r"^\d+\.\d+$", value):
            value = cast_if_possible(float, value)

        if (value in _types.keys()):
            value = _types[value]

        output[key] = value
    return output


def dump(obj: LoadDict, fp: TextIO) -> None:
    fp.write(dumps(obj))


def dumps(obj: LoadDict) -> str:
    output: str = ""
    for key, value in obj.items():
        try:
            for _key, _value in _types.items():
                if value == _value:
                    value = _key
        except ValueError:
            continue
        if key == "#":
            output += f"#{value}\n"
        else:
            output += f"{key}={value}\n"
    return output
