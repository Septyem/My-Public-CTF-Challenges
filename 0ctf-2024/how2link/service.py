#!/usr/bin/python3
import os
import sys
import random
import signal
import string
import tempfile
import subprocess
from hashlib import sha256

from secret import flag

assert len(flag) > 0

MAXFILESZ = 10000

def proof_of_work():
    proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
    digest = sha256(proof.encode('latin-1')).hexdigest()
    sys.stdout.write("sha256(XXXX+%s) == %s\n" % (proof[4:],digest))
    sys.stdout.write('Give me XXXX:')
    sys.stdout.flush()
    x = sys.stdin.readline()
    x = x.strip()
    xx = x+proof[4:]
    if len(x) != 4 or sha256(xx.encode('latin-1')).hexdigest() != digest:
        return False
    return True

def main():
    tempdir = tempfile.mkdtemp()
    signal.alarm(120)
    sys.stdout.write("I have two object files. Can you combine them into one for me\n")
    sys.stdout.flush()
    try:
        size = int(sys.stdin.readline())
        assert size < MAXFILESZ
        res = sys.stdin.read(2*size+1)
        dat = bytes.fromhex(res.strip())

        fname = os.path.join(tempdir, "input")
        with open(fname, "wb") as f:
            f.write(dat)

        sys.stdout.write("Ok I'll try it now\n")
        sys.stdout.flush()
        res = subprocess.call(["./not_linker", fname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        assert res == 0
        res = subprocess.call(["ld", "out.o", "-dynamic-linker", "/lib64/ld-linux-x86-64.so.2", "-lc", "-o", "a.out", "/usr/lib/Scrt1.o"])
        assert res == 0
        res = subprocess.call(["./a.out"])
    except:
        pass
    finally:
        subprocess.call(["rm", "-r", tempdir])

if __name__ == "__main__":
    if proof_of_work():
        main()
