import networkx as nx
from random import randint, choice
from string import hexdigits
from networkx.classes.function import neighbors
from subprocess import run, check_output
import os
import binascii
from functools import partial
import asyncio, socket


import atexit

created_challenges = []

@atexit.register
def cleanup():
	# we clean up files at the end of each round but to prevent accumulation over time lets also do it onexit in case of exceptions and the like
	global created_challenges
	for chall in created_challenges:
		run(f"rm -f /tmp/{chall}*",shell=True)

N = 1000
M = N * 1

def get_path(g):
    while True:
        start = randint(0,N - 1)
        end = randint(0, N - 1)
        try:
            path = nx.algorithms.shortest_paths.generic.shortest_path(g, start, end)
        except:
            continue
        if len(path) > 10:
            return (start, end, path)
    
def get_func(idx, neighbors):
    neighbors = "\n".join([f"\t\tcase {i}: function_{i}(); break;" for i in neighbors])
    next_expr = f"next {choice('^+-')}= {randint(0,2**32-1)};"
    return f"""
void function_{idx}() {{
    uint32_t next = 0;
    scanf("%u\\n", &next);
    {next_expr}
    switch(next) {{
{neighbors}
        default:
            exit(1);
            break;
    }}
}}
"""

def make_c():
    G = nx.gnm_random_graph(N, M)
    start, end, path = get_path(G)
    source = ""
    source += "#include <stdio.h>\n"
    source += "#include <stdlib.h>\n"
    source += "#include <stdint.h>\n"
    for i in [x for x in G.nodes if x != end]:
        source += f"void function_{i}();\n"
    source += f"int main() {{ setvbuf(stdout, NULL, _IONBF, 0); setvbuf(stdin, NULL, _IONBF, 0); setvbuf(stderr, NULL, _IONBF, 0); function_{start}(); return 1; }}"
    source +=f"void function_{end}() {{ exit(0); }}"
    for i in G.nodes:
        if len(list(G.neighbors(i))) == 0:
            continue
        if i == end:
            continue
        source += get_func(i, list(G.neighbors(i)))
    return source



for i in range(5):
    name = binascii.b2a_hex(os.urandom(15)).decode()
    created_challenges.append(name)
    with open(f"/tmp/{name}.c","w") as f:
        f.write(make_c())
    run(f"gcc /tmp/{name}.c -o /tmp/{name}", shell=True)
    run(f"chmod +x /tmp/{name}",shell=True)
    with open(f"/tmp/{name}","rb") as f:
        print(f.read().hex())
    request = bytes.fromhex(input().rstrip())
    if run([f"/tmp/{name}"],input=request).returncode == 0:
        run(f"rm /tmp/{name}*",shell=True)
    else:
        run(f"rm /tmp/{name}*",shell=True)
        exit(0)

with open("/labyrinth/flag.txt", "r") as f:
    print(f.read())
