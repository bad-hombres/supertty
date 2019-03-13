#!/usr/bin/env python
banner = """ (                                        )
 )\ )                     *   )  *   ) ( /(          )    )
(()/(  (          (  (  ` )  /(` )  /( )\())   )  ( /( ( /(
 /(_))))\ `  )   ))\ )(  ( )(_))( )(_)|(_)\   /(( )\()))\())
(_)) /((_)/(/(  /((_|()\(_(_())(_(_())_ ((_) (_))((_)\((_)\\
/ __(_))(((_)_\(_))  ((_)_   _||_   _\ \ / / _)((_) (_)  (_)
\__ \ || | '_ \) -_)| '_| | |    | |  \ V /  \ V /| || () |
|___/\_,_| .__/\___||_|   |_|    |_|   |_|    \_/ |_(_)__/
         |_|
         (c) Bad Hombres 2017
"""
import sys, os, signal, lib, argparse
print banner
handler = None

args = argparse.ArgumentParser(description="Reverse shell catcher")
args.add_argument("--handler", help="Name of the handler module to use")
opts, handler_args = args.parse_known_args()
if not opts.handler:
    args.print_usage()
    sys.exit(1)

def sigint_handler(signal, frame):
    print "!!!!!SIGINT!!!!!"
    if handler: handler.stop()
    sys.exit()

signal.signal(signal.SIGINT, sigint_handler)
upgrader = lib.ShellUpgrader()

try:
    handler = lib.get_handler(opts.handler, handler_args)
    handler.start(upgrader)
except Exception as ex:
    print "[!] An unexpected error occurred: {}".format(ex)
finally:
    if handler: handler.stop()
    upgrader.reset_local(banner + "\n" + "[+] Hack el planeta!..... ")
    os._exit(0)
