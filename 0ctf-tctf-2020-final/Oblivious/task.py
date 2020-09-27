import os
from hashlib import sha256
import SocketServer
from random import seed,randint
from flag import flag
from datetime import datetime
import signal

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
        p = 143076479400112754668374434950545953815136684437666108414660679206211091483848710948823278452160588332574629948804761979007643431742525187661993330603052446962501345077468509959825681071149997647681355309561697446323383797573015653059492709325956269605890293418112765159615661820641395942022030058259368804693
        q = 136554051901741956086434385093165282452866901520432821814824808437137742607696358074868419686686986071172194919133091603769307486592925135977451789526702635678361614724769238792510306390040229752340382614596327436873492443368719052619386508197910372586656310611284765547737523660827703807683987520014518782899
        self.p = p
        self.q = q
        self.n = p*q
        self.e = 0x10001
        self.d = 385166753256123900955983793465278657359454464613009991632541610125750067048792015161046383566348850715574583209055358115096236684957684488252647442623449611777891013980908838678550725247730775346082842570815778044117975837799220578230809328523693090424148917938907957333878349482595138391628497259525427128297243142350223762952079977814418443691775760139502753415175453086506379612287157513787721756219220268122825838223822662578049294602125864956020567473162368654513326775210409197468534906115038194754902261660713986960277063810174616428057767922493770897027088303872896854701537373811503516240118049139711765729

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
        signal.alarm(5)
        while r>0:
            res += self.request.recv(r)
            if res.endswith('\n'):
                r = 0
            else:
                r = sz - len(res)
        res = res.strip()
        signal.alarm(0)
        return res

    def handle(self):
        print self.request.getpeername(), datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
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
    HOST, PORT = '0.0.0.0', 10001
    HOST, PORT = '127.0.0.1', 10001
    print HOST
    print PORT
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
