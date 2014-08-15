from JumpScale import j

import paramiko
from binascii import hexlify
import time


class SSH():

    def __init__(self, server, PRIVATEKEY='/root/.ssh/id_rsa'):

        self.PRIVATEKEY = PRIVATEKEY
        self.user = 'root'
        self.server = server
        self.port = 22
        # paramiko.util.log_to_file("ssh.log")
        self.trans = paramiko.Transport((self.server, self.port))

        rsa_key = paramiko.RSAKey.from_private_key_file(self.PRIVATEKEY)

        self.checkSSHFirstConnect()

        self.trans.connect(username=self.user, pkey=rsa_key)
        self.session = self.trans.open_session()
        self.session.invoke_shell()
        # print self.receive()

    def checkSSHFirstConnect(self):
        e = j.tools.expect.new("ssh %s" % self.server)
        if e.expect("password:"):
            return
        if e.expect("you sure you want to continue connecting"):
            e.send("yes\n")

    def send(self, cmd):
        self.session.send("%s\n" % cmd)

    def receive(self, timeout=5):
        start = j.base.time.getTimeEpoch()
        while True:
            ready = self.session.recv_ready()
            readysterr = self.session.recv_stderr_ready()
            if ready or readysterr:
                break
            time.sleep(0.1)
            now = j.base.time.getTimeEpoch()
            if now > start + timeout:
                raise RuntimeError("Timeout on receiving")
        out = ""
        if readysterr:
            while True:
                outItem = self.session.recv_stderr(5000)
                out += outItem
                if self.session.recv_stderr_ready() == False:
                    break
                time.sleep(0.01)
        if ready:
            while True:
                outItem = self.session.recv(5000)
                out += outItem
                if self.session.recv_ready() == False:
                    break
                time.sleep(0.01)
        return out

    def changePasswd(self, newPasswd):

        passwd = newPasswd
        self.send("passwd root")

        for i in range(2):
            out = self.receive()
            if out.find("password:") != -1:
                self.send(passwd)
            else:
                raise RuntimeError("Could not change root passwd")

        out = self.receive()
        if out.find("password updated successfully") == -1:
            raise RuntimeError("Could not change root passwd")

# ssh=SSH('37.139.2.78')
# ssh.changePasswd("Dct007")
