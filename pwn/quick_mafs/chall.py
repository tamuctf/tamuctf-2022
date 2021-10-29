from random import randint, choice, shuffle
import sys, os, binascii
from subprocess import run, PIPE
from struct import unpack
MAX_NUM = 0xffff
ARITH_STEP_LENGTH = 10

# pls don't judge my shit code :)

import atexit

created_challenges = []

@atexit.register
def cleanup():
	# we clean up files at the end of each round but to prevent accumulation over time lets also do it onexit in case of exceptions and the like
	global created_challenges
	for chall in created_challenges:
		run(f"rm -f /tmp/{chall}*",shell=True)

def make_operations():

	def get_inverse(op):
		return {
			"ADD": "SUB",
			"SUB": "ADD",
			"XOR": "XOR"
		}[op]

	target = randint(0,MAX_NUM)
	operations = []
	current = target
	for i in range(ARITH_STEP_LENGTH):
		op = choice(["ADD", "SUB", "XOR"])
		rhs = randint(0,MAX_NUM)
		operations.append((get_inverse(op), rhs))
		current = {
			"ADD": lambda x, y: (x + y) & MAX_NUM,
			"SUB": lambda x, y: (x - y) & MAX_NUM,
			"XOR": lambda x, y: (x ^ y) & MAX_NUM,
		}[op](current, rhs)

	return (current, target, operations[::-1])

for i in range(5):
	start, target, operations = make_operations()
	print(f"call print() with rax = {hex(target)}")

	operations += [(choice(["ADD", "SUB", "XOR"]), randint(0,MAX_NUM)) for x in range(150)]
	shuffle(operations)
	op_gadgets = [f"\"lea rbx, [constants + 2 * {idx}];{op} ax, [rbx]; ret;\"" for idx, (op, rhs) in enumerate(operations)]
	constants = ",".join([f"{rhs}U" for op, rhs in operations])
	op_gadgets = [f"\"mov rax, {hex(start)}; ret;\""] + op_gadgets
	code = """

	unsigned short constants[160] = {{{}}};

	void gadgets() {{
		asm(
	{}
		);
	}}

	void print() {{
		asm
	    (	

	    	"mov rdx, 2;"
	    	"push rax;"
	    	"mov rsi, rsp;"
	    	"mov rdi, 1;"
	        "mov rax, 1;"
	        "syscall;"
	       	"mov rdi, 0;"
	        "mov rax, 60;"
	        "syscall;"
	    );
	}}


	int vuln() {{
    	asm
	    (
	        "mov rax, 0;"
	        "mov rdi, 0;"
	        "mov rsi, rsp;"
	        "mov rdx, 0x2000;"
	        "syscall;"
	    );
	}}

	int _start() {{
		vuln();
		asm("mov rax, 0;");
	}}

	""".format(constants, '\n'.join(op_gadgets))

	name = binascii.b2a_hex(os.urandom(15)).decode()
	created_challenges.append(name)
	with open(f"/tmp/{name}.c","w") as f:
		f.write(code)
	run(f"gcc -masm=intel -no-pie -nostdlib /tmp/{name}.c -o /tmp/{name}",shell=True, capture_output=True)
	run(f"chmod +x /tmp/{name}",shell=True, capture_output=True)
	with open(f"/tmp/{name}","rb") as f:
		print(f.read().hex())

	request = bytes.fromhex(input().rstrip())
	result = unpack("<H", run(f"/tmp/{name}", input=request, shell=True, capture_output=True).stdout)[0]
	os.system(f"rm /tmp/{name}*")
	if  result == target:
		continue
	print("sorry you didn't pwn it right :(")
	exit(0)


with open("/pwn/flag.txt","r") as f:
	print(f.read())

