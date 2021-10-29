from pwn import *

p = remote("tamuctf.com", 443, ssl=True, sni="unboxing")
for binary in range(5):
  with open("elf", "wb") as file:
    file.write(bytes.fromhex(p.recvline().rstrip().decode()))

  # send whatever data you want
  p.sendline(b"howdy".hex())
  p.recvline() # receive response from the server. the binary will respond with either "correct :)" or "wrong :(" depending on the exit code

p.interactive()