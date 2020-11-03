
from typing import Dict, List, Text, TextIO, Union
import json
_loaddict = Dict[str, Union[str, int, float, bool]]
_types = {
    "true": True,
    "false": False,
    "null": None
}

def load(file: TextIO) -> _loaddict:
    return loads(file.read())

def loads(string: str) -> _loaddict:
    output: _loaddict = {}
    for line in string.splitlines():
        key, value = line.strip().split("=")

        if (value in _types.keys()):
            value = _types[value]
        output[key] = value
    return output

def dump(obj: _loaddict, fp: TextIO) -> None:
    
    dumps(obj)

def dumps(obj: _loaddict) -> str:
    output: str = ""
    for key, value in obj:
        try:
            value = list(_types.keys())[list(_types.values()).index(value)]
        except IndexError:
            pass
    return output