# INDie COmpany Internal Message #122521
---

## To: Dr Friedman
## From: [REDACTED]

## Details
We finally found that document you were looking for. 
It exists!
However it's written in code; you're the best cryptographer we have.
Decode it and get that flag!

`crypto/indie-co/data.txt`

## Hints
1. Dr Friedman was a real person
2. The flag is at the end of the file
3. The values might need some fine tuning

## Solution

(courtesy of anomie)

We are given a really long ciphertext, and the curly braces at the end suggest our flag is in there.
Some googling about friedman cryptography reveals a wikipedia for William F. Friedman, which contains mention of his the cryptanalysis tool "index of coincidence". Some more googling reveals that the index of coincidence can be used to estimate the key length of a vigenere cipher.

Used this script to find at where the IoC is the highest:
``` py
import string

alph = list(string.ascii_uppercase)

def getIOC(text):
	letterCounts = []

	# Loop through each letter in the alphabet - count number of times it appears
	for i in range(26):
		count = 0
		for j in text:
			if j == alph[i]:
				count += 1
		letterCounts.append(count)

	# Loop through all letter counts, applying the calculation (the sigma part)
	total = 0
	for i in range(len(letterCounts)):
		ni = letterCounts[i]
		total += ni * (ni - 1)

	N = len(text)
	c = 26.0 # Number of letters in the alphabet
	total = float(total) / ((N * (N - 1)))
	return total


def getAvgIOC(array):
    tot = 0.0
    for i in array:
        tot += getIOC(i)
    return tot/len(array)

with open('./data.txt', 'r') as inF:
    data = inF.read().replace('{','').replace('}','')
    print(getIOC(data))
    for i in range(1, 30):
        temp = ['']*i
        for j,c in enumerate(data):
            temp[j%i] += c
        print(i, getAvgIOC(temp))
```

It appears that our key is 12 characters long. Using this tool: https://www.dcode.fr/vigenere-cipher and choosing the option for knowing the key length, it gives us the key: `MKWOFVNJOJUO`. Use cyber chef to decode. Strangely, the part inside the curly braces didn't decode correctly, but adding an extra character right after the opening curly brace gives the rest of the flag. Presumably this is an issue of cyber chef not decoding the curly brace so it doesn't move to the next character of the key, but the vigenere implementation to create the ciphertext probably did.

Flag: `gigem{deepfriedmanindexofcoincidence}`
