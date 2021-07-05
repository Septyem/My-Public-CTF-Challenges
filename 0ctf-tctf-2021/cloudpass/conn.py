from pwn import *
from hashlib import sha256
import time

context.log_level='debug'

def dopow(c):
    chal = c.recvline()
    post = chal[12:28]
    tar = chal[33:-1]
    c.recvuntil(':')
    found = iters.bruteforce(lambda x:sha256(x+post).hexdigest()==tar, string.ascii_letters+string.digits, 4)
    c.sendline(found)

c = remote('111.186.59.1', 10001)
dopow(c)
with open('output.kdbx','rb') as f:
    kdbx = f.read()
    
c.sendlineafter('password: ', 'qweqwe')
c.sendlineafter('(y/N) ', 'y')
c.sendlineafter('size: ', str(len(kdbx)))
c.sendlineafter('(hex): ', kdbx.encode('hex'))

c2 = remote('111.186.59.1', 10001)
dopow(c2)
c2.sendlineafter('password: ', 'qweqwe')
c2.sendlineafter('> ', 'list_entries')

c.sendlineafter('> ','gimme_flag')
time.sleep(0.5)

c2.sendlineafter('> ', 'leave')
c2.sendlineafter('(y/N) ', 'y')
db0 = c2.recvline().strip().decode('hex')
with open('output0.kdbx','wb') as f:
    f.write(db0)
c2.close()

c.sendlineafter('> ','add_binary')
p = 'a'*3000
c.sendlineafter('size: ', str(len(p)))
c.sendlineafter('(hex): ', p.encode('hex'))
c.sendlineafter('> ', 'leave')
c.sendlineafter('(y/N) ', 'y')
db1 = c.recvline().strip().decode('hex')
with open('output1.kdbx','wb') as f:
    f.write(db1)


import os
os.system("python dump.py output0.kdbx dump0")
os.system("python dump.py output1.kdbx dump1")
os.system("python solve.py")
