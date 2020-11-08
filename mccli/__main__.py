from mccli.utils import VERSION
from .commands import *
from .cli_parser import run_parser

if __name__ == "__main__":
    print("MCCLI Version", VERSION, end="\n\n")
    run_parser()
