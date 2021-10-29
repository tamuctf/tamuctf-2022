#!/usr/bin/python3

from pwn import *
from capstone import *
from subprocess import run

r = remote("tamuctf.com", 443, ssl=True, sni="unboxing")

for idx in range(5):

    with open(f"elf", "wb") as file:
        file.write(bytes.fromhex(r.recvline().rstrip().decode()))
    exe = ELF(f"elf")

    md = Cs(CS_ARCH_X86, CS_MODE_64)

    data = exe.read(exe.symbols['check'],(43 + 25) * 1024)
    constraints = []
    for i in range(1024):
        xor_remaining = int(next(x for x in md.disasm(data[:25], 0) if x.mnemonic == 'xor').op_str.split(", ")[1],16)
        data = bytes([x^xor_remaining for x in data[25:]])
        instrs = list(md.disasm(data[:43], 0))
        try:
            flag_idx = int(instrs[0].op_str.split(" + ")[1][:-1],16)
        except Exception as e:
            flag_idx = 0
        compare = int(instrs[2].op_str.split(", ")[1],16)
        try:
            out_idx = int(instrs[3].op_str.split(" + ")[1][:-1],16)
        except Exception as e:
            out_idx = 0
        constraints.append((flag_idx, compare, out_idx))
        data = data[43:]


    required_outputs = [0 if x == '' else int(x,16) for x in run(f"objdump -Mintel -D ./elf | rg \".*?movzx.*?output(\+?.*?)>\" -r '$1' ",shell=True, stdout=PIPE, stderr=PIPE).stdout.decode().split('\n')[:-1]]
    flag = [0 for x in range(64)]


    map_constraints = {output_idx: (flag_idx, val) for (flag_idx, val, output_idx) in constraints}
    for i in required_outputs:
        flag_idx, val = map_constraints[i]
        if flag[flag_idx] != 0:
            print("overconstrained??")
            exit(1)
        flag[flag_idx] = chr(val)
    
    flag = ''.join(flag)
    print(f'trying {flag}')
    r.sendline(flag.encode().hex())
r.interactive()
