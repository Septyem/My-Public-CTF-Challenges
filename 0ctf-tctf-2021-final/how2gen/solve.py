from pwn import *
import zlib
from subprocess import check_output
from hashlib import sha256

#context.log_level='debug'

def dopow(c):
    chal = c.recvline()
    post = chal[12:28]
    tar = chal[33:-1]
    c.recvuntil(':')
    found = iters.bruteforce(lambda x:sha256(x+post).hexdigest()==tar, string.ascii_letters+string.digits, 4)
    c.sendline(found)

#c = remote('127.0.0.1',10055)
c = remote('121.5.253.92',10001)
dopow(c)

c.recvuntil('today:\n')
gram = c.recvuntil('\nEOF\n')[:-5]
f = open('grammar','w')
f.write(gram)
f.close()

p = check_output(["./a.py"])
print('ready')
p = zlib.compress(p)
print len(p)
c.sendlineafter('size: ', str(len(p)))
c.sendlineafter('(hex): ', p.encode('hex'))

c.interactive()
