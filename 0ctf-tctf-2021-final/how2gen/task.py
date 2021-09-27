#!/usr/bin/python3
import os
import socketserver
import random
import signal
import string
from hashlib import sha256
import zlib
from datetime import datetime
import lark

from flag import flag

N = 0x1000
MAXSIZE = 0x200000

prim = ["LETTER", "WORD", "NUMBER", "DIGIT"]
ops = "!@#$%^&*-+~"
def prob(num):
    if random.randint(0,99)<num:
        return True
    else:
        return False

def genstr():
    return "".join([random.choice(string.ascii_letters+string.digits) for _ in range(random.randint(3,6))])

def genexpr():
    res = ""
    res += random.choice(prim)
    res += " "
    for i in range(random.randint(2,4)):
        res += '"'+random.choice(ops)+'"'
        res += " "
        if prob(80):
            res += random.choice(prim)
        else:
            res += "expression"
        res += " "
    return res

def genstmt():
    res = ""
    res += '"'+genstr()+'"'
    res += " "
    laststr = True
    for i in range(random.randint(3,8)):
        if not laststr and prob(60):
            res += '"'+genstr()+'"'
            laststr = True
        else:
            x = random.randint(0,99)
            if x<60:
                res += "expression"
            elif x<90:
                res += random.choice(prim)
            else:
                res += "statement"
            laststr = False
        res += " "
    return res

def gen_grammar():
    gram = '''%import common.LETTER
%import common.WORD
%import common.NUMBER
%import common.DIGIT
%import common.WS
%ignore WS

start: statement+

'''
    num = 0
    exprs = "expression: "
    for i in range(50):
        if i!=0:
            exprs += "    | "
        exprs += genexpr()
        exprs += "-> cov_%d" % num
        num += 1
        exprs += "\n"
    gram += exprs
    stmts = "statement: "
    for i in range(100):
        if i!= 0:
            stmts += "    | "
        stmts += genstmt()
        stmts += "-> cov_%d" % num
        num += 1
        stmts += "\n"
    gram += stmts
    return gram

def collect_cov(ast):
    cov = 0
    if isinstance(ast, lark.tree.Tree):
        for ch in ast.children:
            cov |= collect_cov(ch)
        if ast.data.startswith('cov_'):
            num = int(ast.data[4:])
            cov |= (1<<num)
    return cov

class Task(socketserver.BaseRequestHandler):
    def proof_of_work(self):
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
        digest = sha256(proof.encode('latin-1')).hexdigest()
        self.request.send(str.encode("sha256(XXXX+%s) == %s\n" % (proof[4:],digest)))
        self.request.send(str.encode('Give me XXXX:'))
        x = self.request.recv(10).decode()
        x = x.strip()
        xx = x+proof[4:]
        if len(x) != 4 or sha256(xx.encode('latin-1')).hexdigest() != digest:
            return False
        return True

    def askfor(self, msg):
        self.request.sendall(msg)
        return self.request.recv(0x20).strip().decode('latin-1')

    def recvint(self):
        try:
            return int(self.request.recv(10))
        except:
            return 0

    def recvcode(self):
        self.request.sendall(b"size: ")
        sz = self.recvint()
        assert sz < MAXSIZE
        self.request.sendall(b"code(hex): ")
        sz = 2*sz+1
        r = sz
        res = b''
        while r>0:
            res += self.request.recv(r)
            r = sz - len(res)
        dat = bytes.fromhex(res.strip().decode('latin-1'))
        dat = zlib.decompress(dat)
        return dat.split(b'|')

    def handle(self):
        signal.alarm(600) # in case you want to use those SLOW python generator
        if not self.proof_of_work():
            return
        print(datetime.now(), self.client_address)
        gram = gen_grammar()
        self.request.sendall(b"your grammar today:\n%s\nEOF\n"%(gram.encode('latin-1')))
        parser = lark.Lark(gram)
        codes = self.recvcode()
        assert len(codes)==N
        signal.alarm(0)
        self.request.sendall(b"running\n")
        found = set()
        ok = True
        tot = 0
        for i in range(N):
            one = codes[i].decode('latin-1')
            try:
                res = parser.parse(one)
                cov = collect_cov(res)
                tot |= cov
                if bin(cov).count('1') < 20:
                    # you assemble it manually?
                    ok = False
                elif cov in found:
                    ok = False
                else:
                    found.add(cov)
            except:
                ok = False
            if not ok:
                break
        if bin(tot).count('1') < 150:
            ok = False
        if ok:
            self.request.sendall(b"%s\n"%(flag))
        else:
            self.request.sendall(b"failed\n")
        self.request.close()

class ForkedServer(socketserver.ForkingTCPServer, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10001
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
