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
        group.add_argument("--stdout-port", type=int, help="Port to listen on for stdout (useful if no pipes are available etc)")
        p.add_argument("--handler-help", action="store_true")
        p.add_argument("--verbose", action="store_true")
        return p

    def get_process_commands(self):
        pass

    def get_output(self):
        try:
            out = self.stdout.read()
            return out
        except IOError:
            return None

    def send_command(self, command):
        self.stdin.write("{}\n".format(command))
        self.stdin.flush()

    def send_command_get_output(self, command, timeout = 1):
        self.send_command(command)
        out = self.get_output()
        i = 0
        while out is None:
            if i >= timeout: break
            time.sleep(1)
            i += 1
            out = self.get_output()

        return out

    def wait_for_connection(self):
        raise "Please Implement wait_for_connection in derived classes..."

    def setup_processes(self):
        process_info = self.get_process_commands()
        print process_info
        self.processes = []

        for i, p in enumerate(process_info):
            if i > 1: break
            tmp = subprocess.Popen(p, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, stdin = subprocess.PIPE)
            fcntl.fcntl(tmp.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
            self.processes.append(tmp)

        self.stdin = self.processes[0].stdin
        if len(self.processes) == 2: 
            self.stdout = self.processes[1].stdout
        else:
            self.stdout = self.processes[0].stdout

    def start(self, upgrader):
        self.setup_processes()
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
            self.stdin.write(line)

    def stop(self):
        for p in self.processes:
            p.kill()
