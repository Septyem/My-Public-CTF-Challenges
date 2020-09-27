The original idea is the MSB of randint(0,n) can be biased for most n in RSA. And if you collect sufficient data it can be used as an oracle for this bit under certain condition.

At this challenge, the LSB is also mixed with MSB, which reduces to usual parity oracle of RSA.

Now the problem is, why would I choose to use Python random module???

> Reference: [Balsn CTF 2019 - unpredictable](https://sasdf.github.io/ctf/tasks/2019/BalsnCTF/crypto/unpredictable/)
