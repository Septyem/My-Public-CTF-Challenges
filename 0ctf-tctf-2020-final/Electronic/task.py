import os
import SocketServer
import requests
import signal
import hashlib
import string
from random import choice

# === permutation snippets begin ===
# randomly grab some permutations online
# credit to https://github.com/dkales/qarma64-python/blob/master/qarma.py

state_permutation = [0,11,6,13,10,1,12,7,5,14,3,8,15,4,9,2]

def HexToBlock(hexstring):
    return [int(b,16) for b in hexstring]

def BlockToHex(block):
    return "".join([hex(b)[2:] for b in block])

def XorBlocks(a,b):
    return [x^y for x,y in zip(a,b)]

def rot(b, r):
    return ((b << r) | (b >> (4-r))) % 16

def MixColumns_M41(col):
    newcol = [0]*4
    newcol[0] = rot(col[1],1) ^ rot(col[2],2) ^ rot(col[3],3)
    newcol[1] = rot(col[0],3) ^ rot(col[2],1) ^ rot(col[3],2)
    newcol[2] = rot(col[0],2) ^ rot(col[1],3) ^ rot(col[3],1)
    newcol[3] = rot(col[0],1) ^ rot(col[1],2) ^ rot(col[2],3)
    return newcol

def MixColumns(state):
    mixed_state = [0 for _ in range(16)]
    for i in range(4):
        incol = [state[0+i], state[4+i], state[8+i], state[12+i]]
        outcol = MixColumns_M41(incol)
        mixed_state[0+i], mixed_state[4+i], mixed_state[8+i], mixed_state[12+i] = outcol
    return mixed_state

def PermuteState(state):
    return [state[i] for i in state_permutation]

def TweakLFSR(tweak):
    for b in [0,1,3,4,8,11,13]:
        t = tweak[b]
        b3,b2,b1,b0 = (t>>3)&1,(t>>2)&1,(t>>1)&1,(t>>0)&1
        tweak[b] = ((b0^b1)<<3) | (b3 << 2) | (b2<<1) | (b1<<0)
    return tweak

# === permutation snippets end ===

# not really sbox but from random.shuffle
sbox = [232, 140, 98, 54, 175, 224, 2, 37, 139, 108, 225, 99, 80, 208, 18, 186, 206, 101, 58, 190, 92, 7, 125, 194, 204, 163, 198, 106, 222, 13, 231, 164, 135, 196, 153, 148, 173, 185, 69, 200, 215, 64, 122, 170, 161, 188, 68, 142, 119, 79, 151, 65, 21, 51, 77, 60, 17, 205, 117, 120, 102, 184, 100, 33, 216, 87, 63, 74, 48, 240, 243, 44, 127, 1, 43, 203, 86, 195, 141, 228, 132, 128, 145, 16, 150, 4, 52, 23, 220, 84, 177, 178, 12, 183, 230, 223, 171, 218, 8, 85, 248, 25, 124, 71, 187, 172, 126, 42, 155, 14, 90, 30, 229, 217, 160, 116, 110, 197, 83, 245, 255, 236, 95, 89, 214, 167, 247, 53, 226, 234, 238, 32, 149, 165, 24, 41, 162, 62, 104, 242, 40, 9, 29, 78, 11, 174, 22, 6, 189, 159, 176, 59, 244, 136, 199, 252, 45, 105, 5, 129, 221, 123, 210, 152, 72, 227, 181, 147, 235, 112, 81, 55, 180, 36, 118, 168, 250, 76, 39, 27, 121, 246, 57, 31, 20, 241, 61, 46, 182, 66, 26, 28, 237, 19, 111, 15, 67, 144, 211, 91, 233, 3, 154, 34, 254, 157, 193, 93, 96, 137, 191, 94, 169, 103, 179, 156, 138, 38, 251, 219, 253, 143, 239, 201, 109, 133, 35, 166, 158, 130, 202, 97, 0, 134, 207, 131, 47, 73, 213, 192, 50, 82, 107, 56, 212, 75, 88, 209, 113, 249, 49, 115, 114, 70, 10, 146]

MAXSIZE = 1000000

def toy0(pt):
    state = HexToBlock(pt.encode('hex'))
    state = PermuteState(state)
    ct = BlockToHex(state).decode('hex')
    return ct
def toy1(pt):
    state = HexToBlock(pt.encode('hex'))
    state = PermuteState(state)
    state = MixColumns(state)
    ct = BlockToHex(state).decode('hex')
    return ct

def sub(state):
    sub_state = []
    for i in range(0, len(state), 2):
        val = sbox[state[i]*16+state[i+1]]
        sub_state.extend([val/16, val%16])
    return sub_state

def cipher(pt, key):
    '''
    large network traffic can be painful
    I think two rounds shall be enough?
    '''
    state = HexToBlock(pt.encode('hex'))
    roundkey = HexToBlock(key.encode('hex'))
    for _ in range(2):
        state = XorBlocks(state, roundkey)
        roundkey = TweakLFSR(roundkey)
        state = PermuteState(state)
        state = MixColumns(state)
        state = sub(state)
    ct = BlockToHex(state).decode('hex')
    return ct

def emulate(gates, circuit, pt, key):
    '''
    Unit 0-63 as plaintext, 64-127 as key, 128-191 as output ciphertext, 
    which are all arbitrarily set.
    And to keep it simple we will emulate linearly from the beginning.
    Seems not exactly circuit but a weird vm, never mind.
    '''
    units = [0]*(192+len(circuit))
    for i in range(8):
        units[i*8:8+i*8] = map(int, bin(ord(pt[i]))[2:].rjust(8,'0'))
    for i in range(8):
        units[64+i*8:72+i*8] = map(int, bin(ord(key[i]))[2:].rjust(8,'0'))
    for one in circuit:
        gateid = one[0]
        in0 = one[1]
        in1 = one[2]
        out = one[3]
        units[out] = gates[gateid][units[in0]][units[in1]]
    ct = ''
    for i in range(8):
        ct += chr(int(''.join(map(str,units[128+i*8:136+i*8])),2))
    return ct

class Task(SocketServer.BaseRequestHandler):
    def pow(self):
        res = "".join([choice(string.ascii_letters) for i in range(20)])
        self.request.sendall("md5(??????+%s).startswith('000000')" % (res))
        pre = self.request.recv(7).strip()
        return hashlib.md5(pre+res).hexdigest().startswith("000000")

    def recvn(self, sz):
        r = sz
        res = ''
        signal.alarm(10)
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
        self.request.settimeout(60)
        if not self.pow():
            self.request.close()
            return
        try:
            self.request.sendall("Your token: ")
            token = self.recvn(0x20).strip()
            final_size = MAXSIZE
            # get input
            self.request.sendall("gates: ")
            gates = []
            ttables = self.recvn(0x40).split(' ')
            assert len(ttables)<=4
            for ttable in ttables:
                gate = []
                gate.append([int(ttable[0]), int(ttable[1])])
                gate.append([int(ttable[2]), int(ttable[3])])
                gates.append(gate)
            
            self.request.sendall("length: ")
            length = int(self.recvn(0x40))
            self.request.sendall("circuit: ")
            msg = self.recvn(length)

            circuit = []
            for one in msg.split(' '):
                tmp = map(int, one.split(','))
                assert len(tmp)==4 # gateid,in0,in1,out
                circuit.append(tmp)

            # go!
            ok = True
            for i in range(0x100):
                pt = os.urandom(8)
                key = os.urandom(8)
                ct0 = cipher(pt, key)
                ct1 = emulate(gates, circuit, pt, key)
                if ct0 != ct1:
                    ok = False
                    break

            # oh maybe it works for toy examples
            if not ok:
                pt = os.urandom(8)
                ct0 = toy0(pt)
                ct1 = toy1(pt)
                ct2 = emulate(gates, circuit, pt, '\x00'*8)
                if ct2 == ct1:
                    final_size = MAXSIZE - 2
                elif ct2 == ct0:
                    final_size = MAXSIZE - 1
            else:
                final_size = len(circuit)
                
            score = MAXSIZE-final_size    
            self.request.sendall("Your score: %s\n" % score)
            # report the score blah blah
        finally:
            self.request.close()


class ForkedServer(SocketServer.ForkingTCPServer, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10001
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
