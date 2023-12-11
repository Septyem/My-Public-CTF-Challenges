from pwn import *
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
c.sendlineafter('> ', '1')
c.sendlineafter(': ', '3')
c.sendlineafter(': ', '616263')
c.sendlineafter('> ', '1')
c.sendlineafter(': ', '3')
c.sendlineafter(': ', '313233')
c.sendlineafter('> ', '4')
c.recvuntil('size: ')
sz = int(c.recvline())
print(sz)
ctar = c.recvline()
assert len(ctar) == sz*2+1
t = bytes.fromhex(ctar.strip().decode('latin-1'))
with open("a.ctar", 'wb') as f:
    f.write(t)
t = list(t)
t[8] ^= 1
c.sendlineafter('> ', '2')
c.sendlineafter(': ', str(len(t)))
c.sendlineafter(': ', bytes(t).hex())
c.recvuntil("tar file\n")
resp = c.recvline()
t = list(bytes.fromhex(resp.strip().decode('latin-1')))
t[0] ^= 1
with open("a.tar", 'wb') as f:
    f.write(bytes(t))
#c.sendlineafter('> ', '0')
#c.recvuntil('[OK] ')
#fname = c.recv(8)
c.close()


