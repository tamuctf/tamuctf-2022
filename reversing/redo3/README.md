# RE-do 3

## Description
The lord is my shepard, I shall not want;
But my dreams this challenge will haunt.

Elegance and care put into its creation;
just make sure to not fall into stagnation.

## Solution
I didn't feel like manually reversing too much, so I lifted the global data from Ghidra, then wrote a simple brute-forcer. Looking at the decompilation, we know that the first argument is 5 characters and gets repeatedly XORed against the global data, so I assumed there would eventually be a "gigem" somewhere in the output. I also assumed the input argument would be alphanumeric since it was a command-line argument .

```rust
static CODE: [u8; 100] = [
    0xd8, 0xdf, 0xc7, 0xd4, 0xc9, 0xd8, 0xdf, 0xc7, 0xd4, 0xc9, 0xd8, 0xdf, 0xc7, 0xd4, 0xc9, 0xd8,
    0xdf, 0xc7, 0xd4, 0xc9, 0x47, 0xf7, 0x56, 0x44, 0x59, 0x48, 0xf4, 0x57, 0x44, 0x59, 0x48, 0x82,
    0xd7, 0xad, 0x47, 0x48, 0x4f, 0x57, 0xfc, 0x5d, 0x48, 0x4f, 0x57, 0xff, 0x58, 0x48, 0x4f, 0x57,
    0x1d, 0xe3, 0x53, 0x4f, 0x57, 0x44, 0x94, 0xc8, 0xf7, 0x56, 0x44, 0x59, 0x48, 0xf4, 0x57, 0x44,
    0x59, 0x48, 0x82, 0xd7, 0xac, 0x84, 0xb7, 0xb0, 0xa8, 0x23, 0x30, 0x2f, 0x2a, 0x3a, 0x3f, 0x29,
    0x78, 0x7e, 0x39, 0x30, 0x6a, 0x3a, 0x10, 0x3a, 0x25, 0x3e, 0x79, 0x2c, 0x08, 0x34, 0x38, 0x79,
    0x21, 0x24, 0x39, 0x53,
];
static ALPHA: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

fn check(out: &mut [u8; 100], guess: &[u8; 5]) {
    for (out_chunk, code_chunk) in out.chunks_exact_mut(5).zip(CODE.chunks_exact(5)) {
        for ((code, out), guess) in code_chunk
            .iter()
            .copied()
            .zip(out_chunk.iter_mut())
            .zip(guess.iter().copied())
        {
            *out = code ^ guess;
        }
    }
    if out.windows(5).any(|w| w == b"gigem") {
        println!("{}", String::from_utf8_lossy(out));
        std::process::exit(0);
    }
}
fn main() {
    let mut out = [0u8; 100];
    let mut bytes = [0u8; 5];
    for &x in ALPHA {
        bytes[0] = x;
        for &x in ALPHA {
            bytes[1] = x;
            for &x in ALPHA {
                bytes[2] = x;
                for &x in ALPHA {
                    bytes[3] = x;
                    for &x in ALPHA {
                        bytes[4] = x;
                        check(&mut out, &bytes);
                    }
                }
            }
        }
    }
}
```

Flag: `gigem{p01nt3r_mag1c_pa1ns}`
