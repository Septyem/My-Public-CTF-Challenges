from pwn import *
import string
from hashlib import sha256

context.log_level='debug'

def dopow():
    chal = c.recvline()
    post = chal[12:28]
    tar = chal[33:-1]
    c.recvuntil(':')
    found = iters.bruteforce(lambda x:sha256(x+post).hexdigest()==tar, string.ascii_letters+string.digits, 4)
    c.sendline(found)

c = remote('202.120.7.221', 8888)
dopow()
c.recvuntil('OK\n')
with open('app','rb') as f:
    cont = f.read()
c.sendline(str(len(cont)))
c.send(cont)
c.interactive()
