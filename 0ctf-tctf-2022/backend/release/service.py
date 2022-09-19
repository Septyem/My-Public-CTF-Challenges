#! /usr/bin/python2

import subprocess
import tempfile
import sys,os
import random,string
from hashlib import sha256
import shutil

from flag import flag

LLC = "/chal/llc"

def proof_of_work():
    proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in xrange(20)])
    digest = sha256(proof).hexdigest()
    sys.stdout.write("sha256(XXXX+%s) == %s\n" % (proof[4:],digest))
    sys.stdout.write('Give me XXXX:')
    sys.stdout.flush()
    x = sys.stdin.readline()
    x = x.strip()
    if len(x) != 4 or sha256(x+proof[4:]).hexdigest() != digest:
        return False
    sys.stdout.write('OK\n')
    sys.stdout.flush()
    return True

def main():
    try:
        size = int(sys.stdin.readline())
    except:
        return
    if size > 10000:
        return
    exp = sys.stdin.read(size)
    td = tempfile.mkdtemp()
    os.chdir(td)

    with open("test.ll","w") as f:
        f.write(exp)

    try:
        subprocess.check_output([LLC, "-filetype=obj", "-march=chal", "test.ll"])
        subprocess.check_output(["objcopy", "-O", "binary", "--only-section=.text", "test.o", "ans"])
        if os.path.exists("ans"):
            with open("ans") as f:
                cont = f.read()
            if cont == "\x00":
                print(flag)
    finally:
        shutil.rmtree(td)


if __name__ == '__main__':
    if proof_of_work():
        main()

