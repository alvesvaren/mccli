import queue
from subprocess import Popen
import mccli
import subprocess
import sys
import mccli
import os
import time
from threading import Thread
import tty
import termios
import select


# def enqueue_output(out, queue):
#     for line in iter(out.readline, b''):
#         queue.put(line)
#     out.close()

class LocalShell():
    def __init__(self):
        pass

    def run(self):
        env = os.environ.copy()
        p = Popen(["java", "-jar", "server.jar", "nogui"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, env=env)
        sys.stdout.write("Started Local Terminal...\r\n\r\n")

        def writeall(p):
            while True:
                # print("read data: ")
                data = p.stdout.read(1).decode("utf-8")
                if not data:
                    break
                sys.stdout.write(data)
                sys.stdout.flush()

        writer = Thread(target=writeall, args=(p,))
        writer.start()

        try:
            while True:
                d = sys.stdin.read(1)
                if not d:
                    break
                self._write(p, d.encode())

        except EOFError:
            pass

    def _write(self, process, message):
        process.stdin.write(message)
        process.stdin.flush()





def handler(process: Popen):
    while process.poll() is None:
        
        cmd = input("> ").encode("utf-8")
        print(cmd)
        process.stdin.write(cmd + b"\n")
        process.stdin.flush()

def subprocess_open():
    process = subprocess.Popen("java -jar server.jar nogui", stdin=subprocess.PIPE, shell=True, stdout=subprocess.PIPE, env=os.environ.copy())
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

    # shell = LocalShell()
    # shell.run()

def system_open():
    return os.system("java -jar server.jar nogui")

if __name__ == "__main__":
    server = mccli.Server(sys.argv[1])
    os.chdir(server.path)
    if len(sys.argv) > 2:
        if sys.argv[2] == "subproc":
            subprocess_open()
            exit()
    exit(system_open())
