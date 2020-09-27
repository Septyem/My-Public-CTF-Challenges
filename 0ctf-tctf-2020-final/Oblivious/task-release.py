import os
from hashlib import sha256
import SocketServer
from random import seed,randint
from Crypto.Util.number import getStrongPrime, inverse
from flag import flag

BITS = 2048
assert flag.startswith('flag{') and flag.endswith('}')
assert len(flag) < BITS/8
padding = os.urandom(BITS/8-len(flag))
flagnum = int((flag+padding).encode('hex'), 16)

class Task(SocketServer.BaseRequestHandler):
    def genkey(self):
        '''
        NOTICE: In remote server this key is generated like below but hardcoded, since genkey is time/resource consuming
        and I don't want to add annoying PoW, especially for a final event.
        This function is kept for your local testing.
        '''
        p = getStrongPrime(BITS/2)
        q = getStrongPrime(BITS/2)
        self.p = p
        self.q = q
        self.n = p*q
        self.e = 0x10001
        self.d = inverse(self.e, (p-1)*(q-1))

    def genmsg(self):
        '''
        simply xor looks not safe enough. what if we mix adjacent columns?
        '''
        m0 = randint(1, self.n-1)
        m0r = (((m0&1)<<(BITS-1)) | (m0>>1))
        m1 = m0^m0r^flagnum
        return m0, m1

    def recvn(self, sz):
        '''
        add a loop in recv to avoid truncation by network issues
        '''
        r = sz
        res = ''
        while r>0:
            res += self.request.recv(r)
            if res.endswith('\n'):
                r = 0
            else:
                r = sz - len(res)
        res = res.strip()
        return res

    def handle(self):
        seed(os.urandom(0x20))
        self.genkey()
        self.request.sendall("n = %d\ne = %d\n" % (self.n, self.e))
        try:
            while True:
                self.request.sendall("--------\n")
                m0, m1 = self.genmsg()
                x0 = randint(1, self.n-1)
                x1 = randint(1, self.n-1)
                self.request.sendall("x0 = %d\nx1 = %d\n" % (x0, x1))
                v = int(self.recvn(BITS/3))
                k0 = pow(v^x0, self.d, self.n)
                k1 = pow(v^x1, self.d, self.n)
                self.request.sendall("m0p = %d\nm1p = %d\n" % (m0^k0, m1^k1))
        finally:
            self.request.close()


class ForkedServer(SocketServer.ForkingTCPServer, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10002
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
