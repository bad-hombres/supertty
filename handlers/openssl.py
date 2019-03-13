import lib, os, argparse

class Handler(lib.BaseHandler):
    def __init__(self, args):
        super(Handler, self).__init__(args)

        if (not self.args.cert_path or not self.args.key_path):
            if not self.args.host:
                self.key = "{}/key.pem".format(self.args.cert_dir)
                self.cert = "{}/cert.pem".format(self.args.cert_dir)
                print "[+] Generating new cert in {} with subject: {}".format(self.args.cert_dir, self.args.subject)
                os.system("openssl req -x509 -newkey rsa:4096 -keyout {} -out {} -days 365 -nodes -subj {}".format(self.key, self.cert, self.args.subject))
        else:
            self.key = self.args.key_path.name
            self.cert = self.args.cert_path.name

        if self.args.key_path: self.args.key_path.close()
        if self.args.cert_path: self.args.cert_path.close()

    def get_process_command(self):
        if self.args.host:
            return ["openssl", "s_client", "-quiet", "-connect", "{}:{}".format(self.args.host, str(self.args.port))]
        return ["openssl", "s_server", "-quiet", "-key", self.key, "-cert", self.cert, "-port", str(self.args.port), "-naccept", "1"]

    def get_argparser(self):
        p = super(Handler, self).get_argparser()
        p.add_argument("--subject", help="subject of the certificate to generate", default="/C=US/ST=Denial/L=Springfield/O=Dis/CN=www.example.com")
        p.add_argument("--key-path", type=argparse.FileType("r"), help="path to the private key to use (if no generating new)")
        p.add_argument("--cert-path", type=argparse.FileType("r"), help="path to the cert to use (if not generating new")
        p.add_argument("--cert-dir", help="path to store the generated certificates (if key path and cert path not provided", default="/tmp")
        return p

    def wait_for_connection(self):
        while True:
            output = self.get_output()
            if output: break
