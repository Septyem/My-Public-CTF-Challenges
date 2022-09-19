### WARNING: Dirty code 

This target is modified from BPF one. Due to tight schedule, I changed the challenge design several times, and there are likely useless codes all around.

(At first I want to give a pwnable, later to have players compiled a getshell binary, finally producing one byte in .text section will show the flag for you :|)

### How to build

Download [llvm 15.0.0rc3](https://github.com/llvm/llvm-project/releases/download/llvmorg-15.0.0-rc3/llvm-project-15.0.0rc3.src.tar.xz) and add this Target dir. Do not have time to write an automatic build script :(

