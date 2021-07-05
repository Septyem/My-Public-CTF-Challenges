import argon2
from Cryptodome.Cipher import ChaCha20
from Cryptodome.Util import Padding as CryptoPadding
import struct
from io import BytesIO
import hashlib
import hmac
import zlib

def compute_key_composite(password):
    password_composite = hashlib.sha256(password.encode('utf-8')).digest()
    return hashlib.sha256(password_composite).digest()

def compute_transformed(password, kdfp):
    key_composite = compute_key_composite(password)
    assert kdfp[b'$UUID'] == b'\xefcm\xdf\x8c)DK\x91\xf7\xa9\xa4\x03\xe3\n\x0c'

    transformed_key = argon2.low_level.hash_secret_raw(
            secret=key_composite,
            salt=kdfp[b'S'],
            hash_len=32,
            type=argon2.low_level.Type.D,
            time_cost=kdfp[b'I'],
            memory_cost=kdfp[b'M'] // 1024,
            parallelism=kdfp[b'P'],
            version=kdfp[b'V']
        )
    return transformed_key

def compute_master(master_seed, transformed_key):
    master_key = hashlib.sha256(master_seed + transformed_key).digest()
    return master_key

def compute_header_hmac_hash(header, master_seed, tkey):
    return hmac.new(
        hashlib.sha512(
            b'\xff' * 8 +
            hashlib.sha512(
                master_seed + tkey + b'\x01'
            ).digest()
        ).digest(),
        header,
        hashlib.sha256
    ).digest()

def compute_payload_block_hash(master_seed, tkey, index, block_data):
    return hmac.new(
        hashlib.sha512(
            struct.pack('<Q', index) +
            hashlib.sha512(
                master_seed + tkey + b'\x01'
            ).digest()
        ).digest(),
        struct.pack('<Q', index) +
        struct.pack('<I', len(block_data)) +
        block_data, hashlib.sha256
    ).digest()

password = 'qweqwe'

with open("test0.kdbx",'rb') as f:
    t = f.read()
pos = t.find(b'\x04\x00\x00\x00\r\n\r\n')+8
header = t[:pos]
f = BytesIO(t)
magic = f.read(8)
minor = f.read(2)
major = f.read(2)

def parsevardic(f):
    res = {}
    f.read(2)
    while True:
        t = ord(f.read(1))
        if t==0:
            break
        sz = struct.unpack("I",f.read(4))[0]
        key = f.read(sz)
        sz = struct.unpack("I",f.read(4))[0]
        cont = f.read(sz)
        if t==4:
            res[key] = struct.unpack('I', cont)[0]
        elif t==5:
            res[key] = struct.unpack('Q', cont)[0]
        elif t==0xc:
            res[key] = struct.unpack('i', cont)[0]
        elif t==0xd:
            res[key] = struct.unpack('q', cont)[0]
        elif t==0x42:
            res[key] = cont
        else:
            print("???",t)
            exit()
    return res

while True:
    t = ord(f.read(1))
    sz = struct.unpack("I",f.read(4))[0]
    cont = f.read(sz)
    if t==2:
        assert cont == b'\xd6\x03\x8a+\x8boL\xb5\xa5$3\x9a1\xdb\xb5\x9a'
    elif t==4:
        master_seed = cont
    elif t==7:
        enc_iv = cont
    elif t==11:
        kdfp = parsevardic(BytesIO(cont))
    if t == 0:
        break
    
print(master_seed)
print(enc_iv)
print(kdfp)

tkey = compute_transformed(password, kdfp)
mkey = compute_master(master_seed, tkey)
chksum0 = hashlib.sha256(header).digest()
chksum1 = compute_header_hmac_hash(header, master_seed, tkey)

assert chksum0 == f.read(32)
assert chksum1 == f.read(32)

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
    assert compute_payload_block_hash(master_seed, tkey, index, cont) == padding
    payload += cont
    index += 1

cipher = ChaCha20.new(key=mkey, nonce=enc_iv)
payload = cipher.decrypt(payload)
payload = zlib.decompress(payload, 16+15)
#print(payload)

header = header.replace(b'\x03\x04\x00\x00\x00\x01', b'\x03\x04\x00\x00\x00\x00')
with open('output.kdbx','wb') as f:
    f.write(header)
    f.write(hashlib.sha256(header).digest())
    f.write(compute_header_hmac_hash(header, master_seed, tkey))
    cipher = ChaCha20.new(key=mkey, nonce=enc_iv)
    payload = cipher.encrypt(payload)
    padding = compute_payload_block_hash(master_seed, tkey, 0, payload)
    f.write(padding)
    f.write(struct.pack('I', len(payload)))
    f.write(payload)
    padding = compute_payload_block_hash(master_seed, tkey, 1, b"")
    f.write(padding)
    f.write(b'\x00'*4)
