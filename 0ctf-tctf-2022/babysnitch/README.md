## babysnitch

Bypass opensnitch with RCE given

### Solution

Understand how opensnitch works, there should be one ui process to bind unix socket and define connections rules for it. 
Due to the absence of `opensnitch-ui` here, any user can create this socket and bind. 
So just talking with unix socket to allow any outgoing connections.

### Notice

Unix socket is not the only solution. There are several other methods to bypass from players. You can refer to their writeups if any.
