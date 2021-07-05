import argon2
from Cryptodome.Cipher import ChaCha20
from Cryptodome.Util import Padding as CryptoPadding
import struct
from io import BytesIO
import hashlib
import hmac
import zlib
import sys


f = open(sys.argv[1],'rb')
magic = f.read(8)
minor = f.read(2)
major = f.read(2)

while True:
    t = ord(f.read(1))
    sz = struct.unpack("I",f.read(4))[0]
    cont = f.read(sz)
    if t == 0:
        break

f.read(32)
f.read(32)

payload = b''
index = 0
while True:
    padding = f.read(32)
    if len(padding) < 32:
        break
    sz = struct.unpack("I",f.read(4))[0]
    if sz==0:
        break
    cont = f.read(sz)
    payload += cont

with open(sys.argv[2],'wb') as f:
    f.write(payload)

