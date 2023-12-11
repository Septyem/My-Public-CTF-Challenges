from pwn import *
import struct
from hashlib import sha256

def dopow(c):
    chal = c.recvline()
    post = chal[12:28]
    tar = chal[33:-1].decode('latin-1')
    c.recvuntil(':')
    found = iters.bruteforce(lambda x:sha256(x.encode('latin-1')+post).hexdigest()==tar, string.ascii_letters+string.digits, 4)
    c.sendline(found)

context.log_level='debug'

#c = remote("127.0.0.1", 10010)
c = remote("202.120.7.12", 30001)
dopow(c)

omode = b'0000644\x00'
oname = b'51774a47'
tmode = b'\x80\x00\x00\x00\x80\x00\x01\xed'
with open("a.tar", 'rb') as f:
    pt = f.read()
cksum1 = 256 + sum(struct.unpack_from("148B8x356B", pt[0x400:]))
ocksum1 = oct(cksum1)[2:]
assert len(ocksum1) == 5
cksum2 = 256 + sum(struct.unpack_from("148B8x356B", pt[0xc00:]))
ocksum2 = oct(cksum2)[2:]
assert len(ocksum2) == 5
with open("a.ctar", 'rb') as f:
    ct = f.read()
ct = list(ct)

c.sendlineafter('> ', '0')
c.recvuntil('[OK] ')
tname = c.recv(8)
assert len(tname)==8

for i in range(8):
    ct[8+0xc00+i] ^= oname[i]^tname[i]
    cksum2 += tname[i]-oname[i]
for i in range(8):
    ct[8+0x464+i] ^= omode[i]^tmode[i]
    cksum1 += tmode[i]-omode[i]
tcksum1 = oct(cksum1)[2:]
assert len(tcksum1) == 5
tcksum2 = oct(cksum2)[2:]
assert len(tcksum2) == 5
for i in range(5):
    ct[8+0x495+i] ^= ord(ocksum1[i])^ord(tcksum1[i])
for i in range(5):
    ct[8+0xc95+i] ^= ord(ocksum2[i])^ord(tcksum2[i])
cont = bytes(ct)
c.sendlineafter('> ', '2')
c.sendlineafter(': ', str(len(cont)))
c.sendlineafter(': ', cont.hex())

c.sendlineafter('> ', '4')
c.recvuntil('size: ')
sz = int(c.recvline())
ctar = c.recvline()
assert len(ctar) == sz*2+1
t = bytes.fromhex(ctar.strip().decode('latin-1'))
t = list(t)
t[8] ^= 1
c.sendlineafter('> ', '2')
c.sendlineafter(': ', str(len(t)))
c.sendlineafter(': ', bytes(t).hex())
c.recvuntil("tar file\n")
resp = c.recvline()
t = list(bytes.fromhex(resp.strip().decode('latin-1')))
t[0] ^= 1
with open("ans.tar", 'wb') as f:
    f.write(bytes(t))
c.close()
