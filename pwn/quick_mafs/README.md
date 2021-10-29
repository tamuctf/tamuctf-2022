# Quick Mafs

## Description

Oops! I dropped all of these arithmetic gadgets. Fortunately there are enough of them that you won't be able to pick out the right ones.... right?

This is an automatic reversing & exploitation challenge. The server will send you (in order) an instruction (they will be in the format "call print() with rax = 0x1234\n") and an ELF binary as a newline terminated hex string. You should analyze the binary, construct a payload to accomplish that, and then send it back to the server as a newline terminated hex string. To receive the flag you will need to do this 5 times within a timeout of 10 minutes. 

## Solution
See `solve.py`.
