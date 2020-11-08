from subprocess import Popen
import subprocess
import os
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
