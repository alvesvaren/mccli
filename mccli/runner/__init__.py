from subprocess import Popen
import subprocess
import os
import time
from threading import Thread


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


def system_open():
    return os.system("java -jar server.jar nogui")

def tmux_fork(name: str) -> int:
    pid = os.fork()
    if pid == 0:
        print("Creating new mccli run session")
        exit_code = os.system(f'/usr/bin/tmux new-session -ds mc-{name} "mccli run {name}"')
        print("Waiting for server to exit")
        if exit_code == 0:
            try:
                while os.system(f"/usr/bin/tmux has-session -t mc-{name}") == 0:
                    time.sleep(1)
                return 1
            except KeyboardInterrupt:
                print("Killing server as process was terminated")
                return os.system(f"/usr/bin/tmux kill-session -t mc-{name}")
        return exit_code
    else:
        exit(0)