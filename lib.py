import os
import sys
import threading
import fcntl
import subprocess
import time
import argparse

def get_handler(handler, args):
    m = __import__("handlers.{}".format(handler), fromlist=[handler])
    return m.Handler(args)

class ShellUpgrader(object):    
    def __init__(self):
        self.needs_reset = False

    def setup(self):
        self.term = os.environ["TERM"]
        self.rows, self.columns = os.popen('stty size', 'r').read().split()
        print "[+] Got terminal: {}".format(self.term) 
        print "[+] Got terminal size {} rows, {} columns".format(self.rows, self.columns) 
        print "[+] Setting up local terminal....."
        os.system("stty raw -echo")
        self.needs_reset = True

    def upgrade_shell(self,handler):
        handler.send_command("python -c 'import pty; pty.spawn(\"/bin/bash\")'")
        time.sleep(2)
        handler.send_command("export TERM={}".format(self.term))
        handler.send_command("export SHELL={}".format("/bin/bash"))
        handler.send_command("stty rows {} columns {}".format(self.rows, self.columns))
        handler.send_command("reset")

    def reset_local(self, message):
        if self.needs_reset:
            print "[+] Resetting local terminal....."
            os.system("stty raw echo")
            os.system("reset")
            self.needs_reset = False
            print message


class GetOutputThread(threading.Thread):
    def __init__(self, handler):
        threading.Thread.__init__(self)
        self.handler = handler

    def run(self):
        print "[+] Output thread started...."
        while True:
            output = self.handler.get_output()
            if output:
                sys.stdout.write(output)
                sys.stdout.flush()

class BaseHandler(object):
    def __init__(self, args):
        parser = self.get_argparser()
        self.args, rest = parser.parse_known_args(args)
        if self.args.handler_help:
            parser.print_help()
            sys,exit(1)

        if not self.args.port:
            parser.print_help()
            sys.exit(1)

    def get_argparser(self):
        p = argparse.ArgumentParser("supertty.py --listener {}".format(type(self).__module__.replace("handlers.", "")), description="Handler")
        required = p.add_argument_group("Required arguments")
        required.add_argument("--port", type=int, help="Port to listen on or connect to")
        group = p.add_mutually_exclusive_group()
        group.add_argument("--host", help="Host to connect to for bind shells")
        group.add_argument("--ip", help="ip to listen on for reverse shells")
        p.add_argument("--handler-help", action="store_true")
        p.add_argument("--verbose", action="store_true")
        return p


    def get_process_commend(self):
        pass

    def get_output(self):
        try:
            out = self.process.stdout.read()
            return out
        except IOError:
            return None

    def send_command(self, command):
        self.process.stdin.write("{}\n".format(command))
        self.process.stdin.flush()

    def wait_for_connection():
        raise "Please Implement wait_for_connection in derived classes..."

    def start(self, upgrader):
        print " ".join(self.get_process_command())
        self.process = subprocess.Popen(self.get_process_command(), stdout = subprocess.PIPE, stderr = subprocess.STDOUT, stdin = subprocess.PIPE)
        fcntl.fcntl(self.process.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        upgrader.setup()
        self.wait_for_connection()
        print "[+] Connection establishd!"
        upgrader.upgrade_shell(self)

        t = GetOutputThread(self)
        t.daemoun = True
        t.start()

        while True:
            line = sys.stdin.read(1)
            if ord(line[0]) in [4]: break
            if line == "": break
            self.process.stdin.write(line)

    def stop(self):
        self.process.kill()
