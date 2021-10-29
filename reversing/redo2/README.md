# RE-do 2

## Description
Honestly this is just a plain an simple ASM challenge.
Best of luck.

## Hints
1. There is a lot of the same pattern in the ASM, take advantage of it
2. Godbolt is a pretty good tool
3. Maybe you don't necessarily need to reverse the entirety of the program, just enough to understand the data

## Solution
angr failed me :cry: 

As above, I compiled the asm to a binary then slapped that bad boy in Ghidra. Extracted the following constraints:

```py
x[1] = ord('8')
x[0] = ord('6')
x[3] = ord('4')
x[5] = ord('J')
x[4] = ord('<')
x[6] = ord('0')
x[7] = ord('0')
x[8] = ord('0')
x[10] = ord('1')
x[11] = ord('1')
x[12] = ord('1')
x[13] = ord('1')
x[15] = ord('2')
x[16] = ord('2')
x[17] = ord('2')
x[18] = ord('2')
x[19] = ord('2')
x[9] = ord('.')
x[0x1b] = 1
x[0x1a] = 2
x[0x17] = 3
x[0x18] = 4
x[0x19] = 0
x[0xe] = x[9]
x[0x14] = x[9]
x[0x16] = x[9]
x[0x15] = x[0xf] + 1
x[28] = x[5] + 2
x[2] = x[0]
```

Then put it in python with:

```py
>>>> x = [0]*0x1d
>>>> ... # copied from above
>>>> "".join([chr(i + 0x31) for i in x])
'gigem{aaa_bbbb_ccccc_d_45132}'
```

Flag: `gigem{aaa_bbbb_ccccc_d_45132}`
