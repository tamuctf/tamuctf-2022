# Vanity

## Description
[Read, weep, seethe, and cope.](https://github.com/tamuctf/vanity)

![](https://c.tenor.com/3BMRCVepIa8AAAAC/vanity-smurf-youre-so-vain.gif)

## Solution
The hint is in the name and the GIF; "vanity" == "mirror". 
```sh
git clone --mirror https://github.com/tamuctf/vanity.git
```
Inspecting the contents of `packed-refs`, we have:
```
# pack-refs with: peeled fully-peeled sorted 
ddf0fc5d6df4c8121a77797ef51f82890a5a461f refs/heads/main
ddf0fc5d6df4c8121a77797ef51f82890a5a461f refs/remotes/origin/main
a26b919a122134988f6df04854363bd43d27673e refs/remotes/origin/sussy
```
The last commit is very sus, so we'll clone the repo for realsies to check out the commit hash:
```sh
git clone ./vanity.git
cd vanity
git checkout a26b919a122134988f6df04854363bd43d27673e
cat sneaky.txt
```

Flag: `gigem{watch_the_night_and_bleed_for_me}`
