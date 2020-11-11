from mccli.server_utils import Server
from mccli.tmux_utils import create_session, get_server, get_session, get_pane
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



def run_jar(name: str):
    server = Server(name)
    process = subprocess.Popen(["java", "-jar", "server.jar", "nogui"], cwd=server.path)
    return process.wait()

def run_tmux(name: str) -> int:
    session_name = "mc-" + name
    print("Creating new mccli run session")
    session = create_session(session_name, f"mccli runner {name}")
    if session:
        def handle_termination(num, stack):
            print("Stopping server")
            get_pane(session).send_keys("stop")

        signal.signal(signal.SIGTERM, handle_termination)
        signal.signal(signal.SIGINT, handle_termination)
        print("Waiting for session to exit (when the server gets stopped)")
        while get_server().has_session(session_name):
            time.sleep(1)
        print("Session stopped")
    else:
        print(f"Session did not start, possibly already a session with the name {session_name}")
        return 1
    return 0
    # exit1 = os.system(f'/usr/bin/tmux new-session -ds mc-{name} "mccli runner {name}"')
    # exit2 = os.system(f'/usr/bin/tmux wait-for mc-{name}-done')
    # exit(exit1 if exit1 != 0 else exit2)
    # print("Waiting for server to exit")
    # if exit_code == 0:
    #     try:
    #         while os.system(f"/usr/bin/tmux has-session -t mc-{name}") == 0:
    #             time.sleep(1)
    #         return 1
    #     except KeyboardInterrupt:
    #         print("Killing server as process was terminated")
    #         return os.system(f"/usr/bin/tmux kill-session -t mc-{name}")
    # return exit_code