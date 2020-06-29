import string
from struct import pack,unpack

P = 247359019496198933
C = 223805275076627807
M = 2**60
K0, K1 = 134854706973672807, 187692079449969593

from Crypto.Util.number import inverse
Ci = 1131579515458719391
K0i = inverse(K0, P)
K1i = inverse(K1, P)

cflag = 'b1b8024cb0079102693cb3a3d8441600201266ef3899e2001bd2c7ed52d45c01f6de2d911b04bc00971842482a650900'.decode('hex')

tab = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
tab = string.printable

#debug
def decrypt_block(x, o=0):
    tmp = x * K1i % P
    tmp += o*P
    tmp = tmp * Ci % M
    tmp = tmp * K0i % P
    return tmp

fmt = '%dQ' % (len(cflag)/8)
blks = unpack(fmt, cflag)
pt = ''
for b in blks:
    found = False
    for o in range(5):
        cur = decrypt_block(b, o)
        while cur < 2**63:
            t = pack('Q', cur)
            if all(map(lambda x:x in tab, t)):
                pt += t
                found = True
                break
            cur += P
    if not found:
        print 'failed'
print pt

