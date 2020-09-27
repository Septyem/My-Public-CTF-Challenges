from pwn import remote, context, iters
from hashlib import md5
import string

#context.log_level='debug'

perm = [0,11,6,13,10,1,12,7,5,14,3,8,15,4,9,2]

sbox = [232, 140, 98, 54, 175, 224, 2, 37, 139, 108, 225, 99, 80, 208, 18, 186, 206, 101, 58, 190, 92, 7, 125, 194, 204, 163, 198, 106, 222, 13, 231, 164, 135, 196, 153, 148, 173, 185, 69, 200, 215, 64, 122, 170, 161, 188, 68, 142, 119, 79, 151, 65, 21, 51, 77, 60, 17, 205, 117, 120, 102, 184, 100, 33, 216, 87, 63, 74, 48, 240, 243, 44, 127, 1, 43, 203, 86, 195, 141, 228, 132, 128, 145, 16, 150, 4, 52, 23, 220, 84, 177, 178, 12, 183, 230, 223, 171, 218, 8, 85, 248, 25, 124, 71, 187, 172, 126, 42, 155, 14, 90, 30, 229, 217, 160, 116, 110, 197, 83, 245, 255, 236, 95, 89, 214, 167, 247, 53, 226, 234, 238, 32, 149, 165, 24, 41, 162, 62, 104, 242, 40, 9, 29, 78, 11, 174, 22, 6, 189, 159, 176, 59, 244, 136, 199, 252, 45, 105, 5, 129, 221, 123, 210, 152, 72, 227, 181, 147, 235, 112, 81, 55, 180, 36, 118, 168, 250, 76, 39, 27, 121, 246, 57, 31, 20, 241, 61, 46, 182, 66, 26, 28, 237, 19, 111, 15, 67, 144, 211, 91, 233, 3, 154, 34, 254, 157, 193, 93, 96, 137, 191, 94, 169, 103, 179, 156, 138, 38, 251, 219, 253, 143, 239, 201, 109, 133, 35, 166, 158, 130, 202, 97, 0, 134, 207, 131, 47, 73, 213, 192, 50, 82, 107, 56, 212, 75, 88, 209, 113, 249, 49, 115, 114, 70, 10, 146]

gid = {}

def cons_perm(inp, outp):
    circuit = ''
    for i in range(16):
        for j in range(4):
            circuit += "%d,%d,%d,%d " % (gid['xor'], inp[4*perm[i]+j], 390, outp[4*i+j])
    return circuit

def cons_xor(inp, key, outp):
    circuit = ''
    for i in range(16):
        for j in range(4):
            circuit += "%d,%d,%d,%d " % (gid['xor'], inp[4*i+j], key[4*i+j], outp[4*i+j])
    return circuit

def cons_mixone(inp, outp, buf):
    circuit = ''
    for i in range(4):
        v0 = inp[4+(i+1)%4]
        v1 = inp[8+(i+2)%4]
        v2 = inp[12+(i+3)%4]
        circuit += "%d,%d,%d,%d " % (gid['xor'], v0, v1, buf)
        circuit += "%d,%d,%d,%d " % (gid['xor'], buf, v2, outp[i])
    for i in range(4):
        v0 = inp[0+(i+3)%4]
        v1 = inp[8+(i+1)%4]
        v2 = inp[12+(i+2)%4]
        circuit += "%d,%d,%d,%d " % (gid['xor'], v0, v1, buf)
        circuit += "%d,%d,%d,%d " % (gid['xor'], buf, v2, outp[4+i])
    for i in range(4):
        v0 = inp[0+(i+2)%4]
        v1 = inp[4+(i+3)%4]
        v2 = inp[12+(i+1)%4]
        circuit += "%d,%d,%d,%d " % (gid['xor'], v0, v1, buf)
        circuit += "%d,%d,%d,%d " % (gid['xor'], buf, v2, outp[8+i])
    for i in range(4):
        v0 = inp[0+(i+1)%4]
        v1 = inp[4+(i+2)%4]
        v2 = inp[8+(i+3)%4]
        circuit += "%d,%d,%d,%d " % (gid['xor'], v0, v1, buf)
        circuit += "%d,%d,%d,%d " % (gid['xor'], buf, v2, outp[12+i])
    return circuit

def cons_mix(inp, outp, buf):
    circuit = ''
    for i in range(4):
        inp0 = inp[4*i:4*i+4] + inp[16+4*i:16+4*i+4] + inp[32+4*i:32+4*i+4] + inp[48+4*i:48+4*i+4]
        outp0 = outp[4*i:4*i+4] + outp[16+4*i:16+4*i+4] + outp[32+4*i:32+4*i+4] + outp[48+4*i:48+4*i+4]
        circuit += cons_mixone(inp0, outp0, buf)
    return circuit

def cons_sub(inp, outp, buf):
    '''
    using [buf, buf+2049]
    suppose they are all 0
    '''
    circuit = ''
    for i in range(8):
        for j in range(8):
            for k in range(256):
                if (k&(1<<(7-j))) != 0:
                    circuit += "%d,%d,%d,%d " % (gid['wtf'], inp[8*i+j], buf+256*i+k, buf+256*i+k)
                else:
                    circuit += "%d,%d,%d,%d " % (gid['or'], inp[8*i+j], buf+256*i+k, buf+256*i+k)
        for k in range(256):
            circuit += "%d,%d,%d,%d " % (gid['inv'], buf+256*i+k, 0, buf+256*i+k)
        for j in range(8):
            # set [buf+2049] = 0
            circuit += "%d,%d,%d,%d " % (gid['xor'], buf+2048, 390, buf+2049)
            for k in range(256):
                if (sbox[k]&(1<<(7-j))) != 0:
                    circuit += "%d,%d,%d,%d " % (gid['or'], buf+256*i+k, buf+2049, buf+2049)
            circuit += "%d,%d,%d,%d " % (gid['xor'], buf+2049, 390, outp[8*i+j])
    return circuit

def cons_tweak(inp, outp):
    circuit = ''
    for b in range(16):
        if b in [0,1,3,4,8,11,13]:
            circuit += "%d,%d,%d,%d " % (gid['xor'], inp[4*b+2], 390, outp[4*b+3])
            circuit += "%d,%d,%d,%d " % (gid['xor'], inp[4*b+1], 390, outp[4*b+2])
            circuit += "%d,%d,%d,%d " % (gid['xor'], inp[4*b+0], 390, outp[4*b+1])
            circuit += "%d,%d,%d,%d " % (gid['xor'], inp[4*b+3], inp[4*b+2], outp[4*b+0])
        else:
            circuit += "%d,%d,%d,%d " % (gid['xor'], inp[4*b+3], 390, outp[4*b+3])
            circuit += "%d,%d,%d,%d " % (gid['xor'], inp[4*b+2], 390, outp[4*b+2])
            circuit += "%d,%d,%d,%d " % (gid['xor'], inp[4*b+1], 390, outp[4*b+1])
            circuit += "%d,%d,%d,%d " % (gid['xor'], inp[4*b+0], 390, outp[4*b+0])
    return circuit

#c = remote('127.0.0.1', 10001)
c = remote('chall.0ops.sjtu.edu.cn', 10001)


def dopow():
    line = c.recvuntil("('000000')")
    post = line[11:31]
    print post
    found = iters.bruteforce(lambda x:md5(x+post).hexdigest().startswith('000000'), string.ascii_letters, 6, method="fixed")
    print found
    c.sendline(found)

dopow()

c.interactive()
exit()

token = 'f5658ad310e0b7e7'
token = '13d83a9ef40967e6'
c.sendlineafter('token: ', token)
ort = '0111'
inv = '1100'
xor = '0110'
wtf = '1101'

gates = ' '.join([ort, inv, xor, wtf])
gid['or'] = 0
gid['inv'] = 1
gid['xor'] = 2
gid['wtf'] = 3

# 390 is always zero
circuit = ''
tmp = range(192,256)
circuit += cons_xor(range(64), range(64,128), tmp)
tmp2 = range(256,320)
circuit += cons_perm(tmp, tmp2)
tmp3 = range(320,384)
circuit += cons_mix(tmp2, tmp3, 384)
circuit += cons_sub(tmp3, tmp, 400)
circuit += cons_tweak(range(64,128), tmp2)
# round2
circuit += cons_xor(tmp, tmp2, tmp)
circuit += cons_perm(tmp, tmp2)
circuit += cons_mix(tmp2, tmp3, 384)
circuit += cons_sub(tmp3, range(128,192), 2500)

c.sendlineafter('gates: ',gates)
c.sendlineafter('length: ', str(len(circuit)))
c.sendlineafter('circuit: ', circuit)
c.interactive()
