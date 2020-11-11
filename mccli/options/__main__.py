from sys import argv
from . import get

if __name__ == "__main__":
    value = get(argv[1])
    if (type(value) == str) and len(argv) > 2:
        value = value.format(*argv[2:])
    print(value)