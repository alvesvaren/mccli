import argparse
from argparse import Namespace
from mccli.tmux_utils import get_server, get_sessions_matching
from .utils import VERSION
import os
import mccli
from pathlib import Path
from .server_utils import Server, get_server_service
from .online_utils import ServerProvider
from .commands import (attach, create, list_command,
                       modify, run, update, runner)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
parser.add_argument("--verbose", "-v", action="store_true")

# Commands that need the server argument to be required
commands = {
    "modify": subparsers.add_parser("modify", aliases=["change"]),
    "update": subparsers.add_parser("update", aliases=["upgrade"]),
    "status": subparsers.add_parser("status"),
    "runner": subparsers.add_parser("runner"),
    "start": subparsers.add_parser("start"),
    "stop": subparsers.add_parser("stop"),
    "disable": subparsers.add_parser("disable"),
    "enable": subparsers.add_parser("enable"),
    "restart": subparsers.add_parser("restart"),
    "attach": subparsers.add_parser("attach", aliases=["console", "a", "c"]),
    "run": subparsers.add_parser("run", aliases=["exec", "execute", "command"])
}

commands_optional_server = {
    "create": subparsers.add_parser("create")
}

commands_no_server = {
    "list": subparsers.add_parser("list")
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
commands["modify"].add_argument(
    "--file", required=False, default="server.properties")

commands["enable"].add_argument("--now", required=False, action="store_true")
commands["disable"].add_argument("--now", required=False, action="store_true")

commands["runner"].add_argument("--tmux", required=False, action="store_true",
                                help="Keep the process alive while the tmux session exists", dest="tmux")

commands["run"].add_argument("command", nargs="+")


def create_wrapper(args: Namespace):
    create(name=args.server, provider=ServerProvider(
        args.provider) if args.provider else None, verbose=args.verbose)


def modify_wrapper(args: Namespace):
    modify(
        name=args.server, key=args.key, value=args.value,
        file_name=args.file, verbose=args.verbose)


def update_wrapper(args: Namespace):
    update(name=args.server, verbose=args.verbose)


def runner_wrapper(args: Namespace):
    runner(name=args.server, in_tmux=args.tmux, verbose=args.verbose)


def run_wrapper(args: Namespace):
    run(name=args.server, command=args.command, verbose=args.verbose)


def attach_wrapper(args: Namespace):
    attach(name=args.server, verbose=args.verbose)


def enable(args: Namespace):
    print(f"Enabling server '{args.server}'")
    get_server_service(args.server).enable(args.now)


def start(args: Namespace):
    print(f"Starting server '{args.server}'")
    get_server_service(args.server).start()


def disable(args: Namespace):
    print(f"Disabling server '{args.server}'")
    get_server_service(args.server).disable(args.now)


def stop(args: Namespace):
    print(f"Stopping server '{args.server}'")
    get_server_service(args.server).stop()


def restart(args: Namespace):
    print(f"Restarting server '{args.server}'")
    get_server_service(args.server).restart()

def status_wrapper(args: Namespace):
    service = get_server_service(args.server)
    print(f"Status for server '{args.server}':")
    print(" - Service state:", service.status.value, f"({service.sub_state})")
    server = Server(args.server)
    print(" - Minecraft version:", server.version)
    print(" - Custom jvm args:", " ".join(server.args), end="\n\n")
    if service.sub_state == "running":
        print(f"* Attach to the server console by typing 'mccli attach {server.name}'")

def list_wrapper(args: Namespace):
    list_command(verbose=args.verbose)

def default_wrapper(args: Namespace):
    print("MCCLI Version", VERSION, end="\n\n")
    parser.print_usage()

commands["create"].set_defaults(runner=create_wrapper)
commands["modify"].set_defaults(runner=modify_wrapper)
commands["update"].set_defaults(runner=update_wrapper)
commands["attach"].set_defaults(runner=attach_wrapper)
commands["status"].set_defaults(runner=status_wrapper)
commands["runner"].set_defaults(runner=runner_wrapper)
commands["enable"].set_defaults(runner=enable)
commands["start"].set_defaults(runner=start)
commands["disable"].set_defaults(runner=disable)
commands["stop"].set_defaults(runner=stop)
commands["restart"].set_defaults(runner=restart)
commands["run"].set_defaults(runner=run_wrapper)
commands["list"].set_defaults(runner=list_wrapper)
parser.set_defaults(runner=default_wrapper)


def run_parser(*args, **kwargs):
    result = parser.parse_args(*args, **kwargs)
    # if result.verbose:
    #     print(result)
    result.runner(result)
