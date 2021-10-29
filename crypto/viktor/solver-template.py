from pwn import *

# This allow for some networking magic 
p = remote("tamuctf.com", 443, ssl=True, sni="viktor")

## YOUR CODE GOES HERE
