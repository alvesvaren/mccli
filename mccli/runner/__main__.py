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

def handler(process: Popen):
    while process.poll() is None:
        
        cmd = input("> ").encode("utf-8")
        print(cmd)
        process.stdin.write(cmd + b"\n")
        process.stdin.flush()

def subprocess_open():
    process = subprocess.Popen(["java", "-jar", "server.jar",
                                "nogui"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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

if __name__ == "__main__":
    server = mccli.Server(sys.argv[1])
    os.chdir(server.path)
    if len(sys.argv) > 2:
        if sys.argv[2] == "system":
            exit(system_open())
    subprocess_open()
    
        

