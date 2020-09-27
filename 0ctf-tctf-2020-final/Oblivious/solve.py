from pwn import *
from math import log,exp

#c = remote('127.0.0.1', 10001)
c = remote('chall.0ops.sjtu.edu.cn', 10002)
c.recvuntil('n = ')
n = int(c.recvline())
ratio = exp(log(2**2047)-log(n))
if ratio<0.7:
    assert False, "bad n"
c.recvuntil('e = ')
e = int(c.recvline())

c.recvuntil('x0 = ')
x0 = int(c.recvline())
c.recvuntil('x1 = ')
x1 = int(c.recvline())

c.sendline(str(x0))

c.recvuntil('m0p = ')
m0p = int(c.recvline())
c.recvuntil('m1p = ')
m1p = int(c.recvline())

def oracle(ct):
    msb = 2**2047
    stats = [0,0]
    cnt = 0
    while cnt < 40 or abs(stats[0]-stats[1])<cnt*0.4*0.6:
        cnt += 1
        c.recvuntil('x0 = ')
        x0 = int(c.recvline())
        c.recvuntil('x1 = ')
        x1 = int(c.recvline())
        c.sendline(str(ct^x0))

        c.recvuntil('m0p = ')
        m0p = int(c.recvline())
        c.recvuntil('m1p = ')
        m1p = int(c.recvline())
        if m1p&msb != 0:
            val = 1
        else:
            val = 0
        val ^= (m0p&1)
        stats[val] += 1
    print stats
    if stats[0] >= stats[1]:
        return 0
    else:
        return 1

upper = n
lower = 0
ct = x0^x1
for i in range(2048):
    print i,'/ tot'
    power = pow(2,(i+1),n)
    _ct = (pow(power, e, n)*ct)%n
    lsb = oracle(_ct)
    if lsb == 0:
        upper = (upper + lower)/2
    else:
        lower = (upper + lower)/2
    if upper < lower:
        break

found = False
for i in range(-1000, 1000):
    if pow(upper+i, e, n) == ct%n:
        found = True
        pt = (upper+i)%n
        break

assert found

m1=m1p^pt
m0=m0p
m0r = (((m0&1)<<2047) | (m0>>1))
flagnum = m0^m0r^m1
print hex(flagnum)
