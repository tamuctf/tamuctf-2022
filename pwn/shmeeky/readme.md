# Shmeeky

## Description
Shared memory vector in kernel space written in 15 minutes?  What could go wrong!

bzImage rootfs.cpio start.sh kernel.diff

log in with user "pwn" and no password

bzImage built by applying kernel.diff to https://github.com/torvalds/linux/commit/40037e4f8b2f7d33b8d266f139bf345962c48d46

rootfs is buildroot 2022.02 with glibc 2.34

## Solution
See `solve.py`.