# What's The Difference

## Description

I made a mistake while making a writeup for a challenge from MetaCTF 2021. Can you find it?

## Solution

Open up the zip and notice that there is a `.git` folder which suggests that the zipped file used to be a git repository. 

Open up README.md to find `Flag: MetaCTF{yOu_w!N_th1$_0n3}` at the end. Clearly, this is not the right flag.

Since we know that this is a git repo, use `git log` to find out what changes were made, and we will see:

```
commit 0b055455560bce16787d2e2a7b0ae36b3ddd2b35 (HEAD, master)
Author: TacEx <TacEx@root.dev>
Date:   Fri Apr 8 02:14:25 2022 -0500

    Whoops wrong flag

commit e61bf8b90c60b29a241bd29205eb173ef79cd850
Author: TacEx <TacEx@root.dev>
Date:   Fri Apr 8 02:13:54 2022 -0500

    Add writeup
```

Use `git checkout e61bf8b90c60b29a241bd29205eb173ef79cd850` to go to the previous version and open `README.md` to find the correct flag at the end.

Flag: `gigem{b3_car3ful_b3for3_y0u_c0mmit}`
