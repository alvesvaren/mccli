import argparse
from argparse import Namespace
import os
import mccli
from pathlib import Path
from mccli.server_utils import Server
from mccli.online_utils import ServerProvider
from .commands import (create, modify, update, run)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
parser.add_argument("--verbose", "-v", action="store_true")

# Commands that need the server argument to be required
commands = {
    "modify": subparsers.add_parser("modify"),
    "update": subparsers.add_parser("update"),
    "status": subparsers.add_parser("status"),
    "run": subparsers.add_parser("run")
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
    run(name=args.server, verbose=args.verbose)


def upgrade(args: Namespace):
    os.chdir(Path(mccli.__file__).parent.resolve())
    exit(os.system("git pull --ff-only"))


commands["create"].set_defaults(runner=create_wrapper)
commands["modify"].set_defaults(runner=modify_wrapper)
commands["update"].set_defaults(runner=update_wrapper)
commands["status"].set_defaults(runner=status_wrapper)
commands["run"].set_defaults(runner=run_wrapper)
commands["upgrade"].set_defaults(runner=upgrade)
parser.set_defaults(runner=status_wrapper)


def run_parser(*args, **kwargs):
    result = parser.parse_args(*args, **kwargs)
    if result.verbose:
        print(result)
    result.runner(result)
