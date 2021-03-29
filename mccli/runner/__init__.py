from mccli.server_utils import Server
from mccli.tmux_utils import create_session, get_server, get_session, get_pane
from mccli.utils import OPTIONS, SERVER_BASE_PATH
from subprocess import Popen
import subprocess
import os
import time
from threading import Thread
import signal


def handler(process: Popen):
    while process.poll() is None:
        cmd = input("> ").encode("utf-8")
        print(cmd)
        process.stdin.write(cmd + b"\n")
        process.stdin.flush()


def subprocess_open():
    process = subprocess.Popen(
        "java -jar server.jar nogui", stdin=subprocess.PIPE,
        shell=True, stdout=subprocess.PIPE, env=os.environ.copy())
    # process.communicate()
    thread = Thread(target=handler, args=[process], daemon=True)
    thread.start()
    try:
        while process.poll() is None:
            # process.communicate(timeout=0.5)
            line = process.stdout.readline()
            if line:
                print(line.decode("utf-8"), end="")
    except KeyboardInterrupt:
        process.kill()


def get_args(server: Server):
    return ["java"] + server.args + ["-jar", "server.jar", "nogui"]


def run_jar(name: str):
    server = Server(name)
    args = get_args(server)
    print("Running jar:", args)
    process = subprocess.Popen(
        args, cwd=server.path)
    return process.wait()


def run_container(name: str):
    server = Server(name)
    args = get_args(server)
    print("Spawning jar in container:", args)
    cmd = f"systemd-nspawn -M mc-{name} --read-only -UD {OPTIONS['paths']['rootfs_image']} \
        --private-users=0 --bind {str(server.path.resolve())}:/server \
        --chdir=/server su minecraft -c \"{' '.join(args)}\""
    print(cmd)
    process = subprocess.Popen(cmd, shell=True)
    return process.wait()


def run_tmux(name: str, container: bool = False) -> int:
    session_name = "mc-" + name
    print("Creating new mccli run session")
    cmd = f"mccli runner {name}"
    if container:
        cmd = f"mccli-priv runner {name} --container"
    session = create_session(session_name, cmd)
    if session:
        def handle_interrupt(num, stack):
            print("Stopping server")
            get_pane(session).send_keys("stop")

        signal.signal(signal.SIGINT, handle_interrupt)
        print("Waiting for session to exit (when the server gets stopped)")
        while get_server().has_session(session_name):
            time.sleep(1)
        print("Session stopped")
    else:
        print(
            f"Session did not start, possibly already a session with the name {session_name}")
        return 1
    return 0
