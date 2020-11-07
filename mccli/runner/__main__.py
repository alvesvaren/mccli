import queue
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

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


if __name__ == "__main__":
    server = mccli.Server(sys.argv[1])
    os.chdir(server.path)
    process = subprocess.Popen(["java", "-jar", "server.jar",
                                "nogui"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        # tty.setcbreak(sys.stdin.fileno())
        cmd = ""
        open("logs/latest.log", "w").close()
        # open("to_run", "w").close()
        with open("logs/latest.log") as file:
            # with open("to_run", "r") as in_file:
            while process.poll() is None:
                # process.stdin.write(line)
                data = file.readline()
                # cmd = in_file.readline()
                # if cmd:
                #     print(cmd)
                    
                #     open("to_run", "wb").close()
                if data:
                    print(data, end="")
                
                # new_cmd = sys.stdin.read(1)
                # if new_cmd:
                #     # print(cmd)
                #     cmd+=new_cmd
                #     if cmd.endswith("\n"):
                #         process.stdin.write(cmd.encode("utf-8"))
                #         cmd = ""
                
    finally:
        process.kill()
    

    process.communicate()
