import lib

class Handler(lib.BaseHandler):
    def __init__(self, args):
        super(Handler, self).__init__(args)

    def get_process_commands(self):
        proclist = []
        args = ["nc"]

        if self.args.host:
            args.append(self.args.host)
            if self.args.udp:
                args.insert(1, "-u")
        else:
            if self.args.udp:
                args.append("-nvlup")
            else:
                args.append("-nvlp")

        args.append(str(self.args.port))
        proclist.append(args)
        if self.args.stdout_port:
            stdout_args = list(args)
            stdout_args[-1] = str(self.args.stdout_port)
            proclist.append(stdout_args)

        if self.args.verbose:
            for args in proclist:
                print "[+] Netcat command: {}".format(" ".join(args))

        return proclist

    def get_argparser(self):
        p = super(Handler, self).get_argparser()
        p.add_argument("--udp", action="store_true", help="listen over udp")
        return p

    def wait_for_connection(self):
        if self.args.host: return
        while True:
            output = self.get_output()
            if output and "connect to" in output:
                break
