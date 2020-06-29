import time
import requests

def parsesig(line):
    a,b = line.strip().split('<br>')
    return str(a[6:]),b[6:].decode('hex')


url = "http://localhost:5000"
url = "http://pwnable.org:10002"
# get base signature
r = requests.get(url+'/register')
m1, sig1 = parsesig(r.text)
# collect 128 signatures
m2 = []
sig2 = []
for i in range(128):
    print(i)
    time.sleep(1)
    r = requests.get(url+'/register')
    m, sig = parsesig(r.text)
    m2.append(m)
    sig2.append(sig)

print(repr(m1))
print(repr(sig1))
print(m2)
print(sig2)
