# Existing Tooling

## Description

Have fun reversing this little crackme. :)

File provided is just the binary.

## Solution
```
❯ gdb existing-tooling --nx --batch --ex "starti" --ex "b *0x00555555554000+0x120d" --ex "c" --ex 'x/s $rbp'

Program stopped.
0x00007ffff7fe3930 in _start () from /lib64/ld-linux-x86-64.so.2
Breakpoint 1 at 0x55555555520d
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".

Breakpoint 1, 0x000055555555520d in ?? ()
0x555555558180:	"gigem{im_curious_did_you_statically_or_dynamically_reverse_ping_addison}"
```
Flag: `gigem{im_curious_did_you_statically_or_dynamically_reverse_ping_addison}`
