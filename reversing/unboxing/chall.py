#!/usr/bin/python3

from random import randint, shuffle
from keystone import *
from os import urandom
from subprocess import run, check_output
import binascii
import atexit

created_challenges = []

@atexit.register
def cleanup():
	# we clean up files at the end of each round but to prevent accumulation over time lets also do it onexit in case of exceptions and the like
	global created_challenges
	for chall in created_challenges:
		run(f"rm -f /tmp/{chall}*",shell=True)

def make_challenge():
	def make_unpack(remaining_count, xor_num):
		return """
		lea rax, [rip+after]
		mov rcx, {}
		loop:
		xor byte ptr [rax], {}
		inc rax
		dec rcx
		jnz loop
		after:
		""".format(remaining_count, xor_num)


	def make_check(flag_idx, output_idx, compare_num):
		return """
		start:
		lea rbx, [r8 + {}]
		mov bl, [rbx]
		xor bl, {}
		lea rcx, [r9 + {}]
		mov byte ptr [rcx], bl
		lea rax, [rip+start]
		mov rcx, 13
		loop:
		mov byte ptr [rax], 0
		inc rax
		dec rcx
		jnz loop
		""".format(flag_idx, compare_num, output_idx)

	def xor_repeated(string, operand):
		return [x^operand for x in string]


	PAD_LEN = 1024

	flag = binascii.b2a_hex(urandom(32))

	bytecode = []

	flag = [(flag[x], x, True) if x < len(flag) else (0, randint(0,64), False) for x in range(PAD_LEN)]
	shuffle(flag)
	checks = []
	ks = Ks(KS_ARCH_X86, KS_MODE_64)
	for (output_idx, (char, idx, isRealChar)) in enumerate(flag):
		if isRealChar:
			checks += [f"output[{output_idx}] == 0"]
		xor_op = randint(0, 255)
		bytecode = xor_repeated(list(bytes(ks.asm(make_check(idx,output_idx,char))[0]).ljust(43,b'\x90')) + bytecode, xor_op)
		bytecode = ks.asm(make_unpack(len(bytecode), xor_op))[0] + bytecode
	bytecode += [0xc3]

	c_src = """
	#include <sys/mman.h>
	#include <stdio.h>
	#include <string.h>
	#include <stdlib.h>

	extern char __executable_start;
	extern char __etext;
	char check[] = {{{}}};

	char input[64];
	char output[{}];

	void main() {{
		void* code = mmap(NULL, sizeof(check), PROT_WRITE | PROT_READ | PROT_EXEC, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
		memcpy(code, &check, sizeof(check));
		read(0, input, 64);
		memset(output, 0, 256);
		__asm__ __volatile__ ( 
			"movq %0, %%r8"
			: : "r"(input) : "memory"
		);
		__asm__ __volatile__ ( 
			"movq %0, %%r9"
			: : "r"(output) : "memory"
		);
		((void (*)()) code)();
		if({}) {{
			puts("correct :)");
			exit(0);
		}} else {{
			puts("wrong :(");
			exit(1);
		}}
	}}

	""".format(", ".join([str(x) for x in bytecode]), PAD_LEN, " && ".join(checks))
	return c_src

for i in range(5):
	code = make_challenge()
	name = binascii.b2a_hex(urandom(15)).decode()
	created_challenges.append(name)
	with open(f"/tmp/{name}.c","w") as f:
		f.write(code)
	run(f"gcc /tmp/{name}.c -o /tmp/{name}",shell=True, capture_output=True)
	run(f"chmod +x /tmp/{name}",shell=True, capture_output=True)
	with open(f"/tmp/{name}","rb") as f:
		print(f.read().hex())

	request = bytes.fromhex(input().rstrip())
	if run(f"/tmp/{name}", input=request, shell=True, capture_output=True).returncode == 0:
		run(f"rm /tmp/{name}*",shell=True)
		continue
	exit(1)

with open("/unboxing/flag.txt", "r") as f:
	print(f.read())