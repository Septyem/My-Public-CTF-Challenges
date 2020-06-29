#!/usr/bin/python2
import random
from struct import pack,unpack

from flag import flag

P = 247359019496198933
C = 223805275076627807
M = 2**60
K0 = random.randint(1, P-1)
K1 = random.randint(1, P-1)

# not a bijection? can be adjusted but I'm lazy
def encrypt_block(x):
    tmp = x * K0 % P
    tmp = tmp * C % M
    tmp = tmp * K1 % P
    return tmp
    
for i in range(2**24):
    pt = random.randint(1, P-1)
    ct = encrypt_block(pt)
    print pt, ct

pt = flag[5:-1]
assert flag.startswith('flag{') and flag.endswith('}') and len(pt)%8==0
fmt = '%dQ' % (len(pt)/8)
ct = pack(fmt, *map(encrypt_block, unpack(fmt, pt)))
print ct.encode('hex')
