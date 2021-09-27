def g(s):
    assert len(s)==14
    res = s[0]&s[1]
    res = (res+s[3])%256
    res ^= (s[5]|s[7])
    res = (res+s[10]+s[11])%256
    return res

s = [187, 169, 20, 23, 100, 94, 107, 117, 131, 108, 239, 63, 106, 112, 155]

for i in range(1234):
    tmp = s[-1]^g(s[:-1])
    s = [tmp]+s[:-1]

flag = 'flag{'+''.join(map(chr,s))+'}'
print flag
    
