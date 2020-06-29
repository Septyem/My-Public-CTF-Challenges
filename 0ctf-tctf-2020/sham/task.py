#!/usr/bin/python3
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import string
import random
import os

from flag import flag
from myhashlib import hash

MAIN_HTML = '''<!DOCTYPE html>
<html>
<body>

<form action="/login">
  <label for="name">name:</label><br>
  <input type="text" id="name" name="name"><br>
  <label for="auth">auth:</label><br>
  <input type="text" id="auth" name="auth"><br><br>
  <input type="submit" value="login">
</form> 
<p>
<a href="/register">register</a>
</p>

</body>
</html>
'''
# NOTICE: secret_key is NOT a constant. (e.g. the server stopped unexpectedly and we restart it later)
secret_key = os.urandom(0x30)

def get_auth(name):
    return hash(secret_key+name)

app = Flask("sham")
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1/second", "300/hour"]
)
@app.route('/')
def main():
    return MAIN_HTML

@app.route('/login')
def login():
    name = request.args.get("name")
    auth = request.args.get("auth")
    try:
        auth = bytes.fromhex(auth)
    except:
        return "?"
    print(request.remote_addr, name, auth)
    if name[:5] == "admin" and get_auth(name.encode('latin-1')) == auth:
        return "lgtm. "+flag
    else:
        return "?"

@app.route('/register')
def register():
    name = "test_"+''.join([random.choice(string.ascii_letters) for _ in range(8)])
    auth = get_auth(name.encode('latin-1'))
    return "name: "+name+"<br>auth: "+auth.hex() 

if __name__ == "__main__":
    #app.run("0.0.0.0", 8080)
    app.run()
