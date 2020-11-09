import mccli
import sys
import os
from . import subprocess_open, system_open, tmux_fork


if __name__ == "__main__":
    server = mccli.Server(sys.argv[1])
    os.chdir(server.path)
    if len(sys.argv) > 2:
        if sys.argv[2] == "subproc":
            subprocess_open()
            exit()
        elif sys.argv[2] == "fork":
            exit(tmux_fork(server.name))
    exit(system_open())
