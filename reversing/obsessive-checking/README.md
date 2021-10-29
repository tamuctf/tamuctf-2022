# Obsessive Checking

Decrypt flag_book.txt.bin using the binary obsessive-checking. I wouldn't try to wait for it though...

Heavily inspired by UTCTF 2022's "eBook DRM". Use that information as you will... :)

## Solution

I used gdb and yoinked the secret key and nonce from memory.
```python
from Crypto.Cipher import AES

with open("flag_book.txt.bin", "rb") as f:
    data = f.read()
    data = data[16:]

cipher = AES.new(bytes.fromhex("ef6b319ae37703b1ec129694de766b9e4f59ec489ef296562773158c3fedb3c6"), AES.MODE_CBC, bytes.fromhex("509570e72f82ecb73d231a80abe75f57"))
print(cipher.decrypt(data).decode())
```
