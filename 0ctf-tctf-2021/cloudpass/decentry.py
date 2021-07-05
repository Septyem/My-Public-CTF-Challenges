from Cryptodome.Cipher import ChaCha20
import hashlib
import base64

stream_key = b'\xf1\xeb\x87\x1fV\xb8>|q%\xb1\xe4\xd3\xf5\xbe\xb2if\xde\xd9\x14pEA\xbdk\xfb\xbd\xe2\xb7\x1b_\xc8D\x15\xa9>\xaf,Z\xca\xcc6\x13\xd3\xd6^\xb4\xbb|\x1dl\x13\x89;\xebp\x0e_\xedz\x8aRA'
key_hash = hashlib.sha512(stream_key).digest()
key = key_hash[:32]
nonce = key_hash[32:44]
cipher = ChaCha20.new(key=key, nonce=nonce)
ct = 'IGAe/wme6ovYA1E/GAm4gGbMgZ4L0w=='
ct = 'IGAe/wmL8bDbMn8oAyKui3zn25IL22N5cNyXWFfejwDGVxLYdRbS36vSF7NytlCTi29CrI1EOvXLNg9O'
pt = cipher.decrypt(base64.b64decode(ct))
print(pt)

