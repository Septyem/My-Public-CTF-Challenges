flag = '[REDACTED]'
flagnum = int(flag.encode('hex'),16)
h = [1]
p = 374144419156711147060143317175368453031918731002211
m = 16077898348258654514826613220527141251832530996721392570130087971041029999399
assert flagnum < m

def listhash(l):
    fmt = "{} "*len(l)
    s = fmt.format(*l)
    return reduce(lambda x,y:x*y,map(hash,s.split(' ')))

num = 0x142857142857142857
for i in range(num):
    x = h[i]*p%m
    x += h[listhash(h)%len(h)]
    x %= m
    h.append(x)

encflag = h[num] ^ flagnum
print encflag
