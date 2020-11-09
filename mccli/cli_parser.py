import argparse
from argparse import Namespace
import os
import re
import mccli
from pathlib import Path
from .server_utils import Server, get_server_service
from .online_utils import ServerProvider
from .commands import (create, modify, update, run)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
parser.add_argument("--verbose", "-v", action="store_true")

# Commands that need the server argument to be required
commands = {
    "modify": subparsers.add_parser("modify"),
    "update": subparsers.add_parser("update"),
    "status": subparsers.add_parser("status"),
    "run": subparsers.add_parser("run"),
    "start": subparsers.add_parser("start"),
    "stop": subparsers.add_parser("stop"),
    "disable": subparsers.add_parser("disable"),
    "enable": subparsers.add_parser("enable"),
    "restart": subparsers.add_parser("restart"),
}

commands_optional_server = {
    "create": subparsers.add_parser("create")
}

commands_no_server = {
    "upgrade": subparsers.add_parser("upgrade")
}

for k, v in commands.items():
    v.add_argument("server")
commands.update(commands_optional_server)
for k, v in commands_optional_server.items():
    v.add_argument("server", default="", nargs="?")
commands.update(commands_no_server)

# Create command
commands["create"].add_argument(
    "--provider", "-p", required=False, choices=[i.value for i in ServerProvider])

commands["modify"].add_argument("key")
commands["modify"].add_argument("value")
commands["modify"].add_argument("--file", required=False, default="server.properties")

commands["enable"].add_argument("--now", required=False, action="store_true")
commands["disable"].add_argument("--now", required=False, action="store_true")

commands["run"].add_argument("--keep-alive", required=False, action="store_true", help="Keep the process alive while the tmux session exists", dest="keepalive")

def create_wrapper(args: Namespace):
    create(name=args.server, provider=ServerProvider(
        args.provider) if args.provider else None, verbose=args.verbose)


def modify_wrapper(args: Namespace):
    modify(
        name=args.server, key=args.key, value=args.value,
        file_name=args.file, verbose=args.verbose)


def update_wrapper(args: Namespace):
    update(name=args.server, verbose=args.verbose)


def status_wrapper(args: Namespace):
    pass


def run_wrapper(args: Namespace):
    run(name=args.server, fork=args.keepalive, verbose=args.verbose)


def upgrade(args: Namespace):
    os.chdir(Path(mccli.__file__).parent.resolve())
    exit(os.system("git pull --ff-only"))


def enable(args: Namespace):
    get_server_service(args.server).enable(args.now)

def start(args: Namespace):
    get_server_service(args.server).start()

def disable(args: Namespace):
    get_server_service(args.server).disable(args.now)

def stop(args: Namespace):
    get_server_service(args.server).stop()

def restart(args: Namespace):
    get_server_service(args.server).restart()

commands["create"].set_defaults(runner=create_wrapper)
commands["modify"].set_defaults(runner=modify_wrapper)
commands["update"].set_defaults(runner=update_wrapper)
commands["status"].set_defaults(runner=status_wrapper)
commands["run"].set_defaults(runner=run_wrapper)
commands["upgrade"].set_defaults(runner=upgrade)
commands["enable"].set_defaults(runner=enable)
commands["start"].set_defaults(runner=start)
commands["disable"].set_defaults(runner=upgrade)
commands["stop"].set_defaults(runner=stop)
commands["restart"].set_defaults(runner=restart)
parser.set_defaults(runner=status_wrapper)


def run_parser(*args, **kwargs):
    result = parser.parse_args(*args, **kwargs)
    if result.verbose:
        print(result)
    result.runner(result)
