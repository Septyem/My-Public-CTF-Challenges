bd = b'a'*3000

import struct
    
cd = b'\x03'+struct.pack('I', len(bd)+1)+b'\x01'+bd
with open('dump0','rb') as f:
    dat0 = f.read()
with open('dump1','rb') as f:
    dat1 = f.read()

from pwn import xor
ks = xor(dat1[:len(bd)], cd)
pt = xor(dat0, ks)
print(pt)
