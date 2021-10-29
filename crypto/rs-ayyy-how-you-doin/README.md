# RSAyyy how you doin?

## Description

We need you to demonstrate your worth as a hacker -- break some 4096-bit RSA keys and we'll know you know your stuff.

Files src/main.rs and Cargo.toml are provided to the user.

## Solution

Out of all the dependencies in `Cargo.toml`, `rngcache` looks particularly sus. Reading the source on [docs.rs](https://docs.rs/rngcache/latest/src/rngcache/lib.rs.html#28) shows that it caches previous calls to `fill_bytes`. Presumably, this compromises secret key generation since the bytes of one prime would be reused with another. To verify this, I printed out the primes by modifying the provided code:
```diff
     let privkey = RsaPrivateKey::new(&mut rng, 4096)?;
+    let primes = privkey.primes();
+    println!("{}", hex::encode(primes[0].to_bytes_be()));
+    println!("{}", hex::encode(primes[1].to_bytes_be()));
```
Sample output:
```
dbaf4f08c4e25b51f319324ab42e7a0e6bb1265fa43fd9f9b38621a1eab004c8ce9d2c5974ea14860ed9b21594e7bed2d757950040fdfbb07da7ad966dd051751b89994319570bd5eb0af808cc42d6d2729ade501bee1937ec0a12796456f6f32507797e5e82788b03aeac7e5531cff8a5d1bda8db206dd2c4356167c8942b543eeab29da399b9ab9b5da351a9ee3a9ba7f8c88c49805499ed31394fe0f6f3fc14636d2c57986e54a0ba26c241657be5a63258d7072470edeac3acf87741268343e2d42730d9b1d73752b21de7390ea7a3e9eb39e1d3cb35d07b040c4bc34d54cf00e69a35dde3a7be2def5932119db567857e7d093f43a6aa2333f24788ec83
dbaf4f08c4e25b51f319324ab42e7a0e6bb1265fa43fd9f9b38621a1eab004c8ce9d2c5974ea14860ed9b21594e7bed2d757950040fdfbb07da7ad966dd051751b89994319570bd5eb0af808cc42d6d2729ade501bee1937ec0a12796456f6f32507797e5e82788b03aeac7e5531cff8a5d1bda8db206dd2c4356167c894b20b84c59be5b0fe0b7298b2cb315c4bfbd769b0d5374d16af2b7b823207192f2d02a0e7d7fc485c91a3fe763f109fd1a88b72577117e03f99254869c3f2d1e594567e748bdbe2e78ffb01435a94e2362413d79d875697a61f262de746fded69fce6bf733f49556bf7c014703aa4a5f2e2a33db2dcb174c87d5d30b6743b4964aff9
```
We can see that the primes generated secret key the primes share several of the most significant bytes, so we know that P and Q are relatively close. As a result, Fermat's algorithm seems like a good candidate. I copied the public key into `tmp.pem` then threw it at [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool) with an extended timeout:
```sh
❯ RsaCtfTool.py --publickey tmp.pem --attack fermat --timeout 600 --private

[*] Testing key tmp.pem.
[*] Performing fermat attack on tmp.pem.
[*] Attack success with fermat method !
```

I saved the printed secret key into `private.pem`, then wrote some Rust to decrypt the challenge string and print out the plaintext (your ciphertext will be different):
```rust
use rsa::{RsaPrivateKey, pkcs1::DecodeRsaPrivateKey, PaddingScheme};

fn main() {
    let secret = RsaPrivateKey::from_pkcs1_pem(include_str!("./private.pem")).unwrap();
    let ct = hex::decode("36f1e2707f446d4f15712cc6253cb8f9a5c55540d418c649d6e122175f52c58246db78fc1260dc8333fe126eb811d622e3149f50eebb35ebe2973816eb7ea6a34892f9a53a518cc4ec3709fc6970148a84bcf23a5d683d5040630b10a691211951f2f5c41476cb4a961cd0c9d30566001da0c45a970d01817f0a5cc773c212b05ad94a201538841bb50bde4cd1d036da4daca6a7837c82de3d483161621ee8e1a53edbf4399bf6f560d2ac2a023311dbb3f20d3ff8b3516971c8383f2704393ad53bc2f62779ea02140afd88f53a6f53ba8936a8c1f418efeb30aeb9949bb8e76034142c8148e706c912272c276a318e69f9734211387baea516c11bdd0703b985b8223f0793b407b144e4630346617a5f23b4cf15548cb8e2a6a4c0bf5b49fdc401526c875caae8f69cd9d9029da25d2b8963bf3f0760745cf423f242cce171604e0c06964d0be75a4237c85b24549ee3aac76305b4a92ae740196a3bdb8f84450f9abb07b04a2c73ad5c581fbd276650ca23e0af597444c2b827e10daaab78bbe69518798ee77d1c8583ee7b422227cb631734dc9e83ee6fd412fa87dd23f09225b3c59c34cb114905aaec11e1038548acc549b3d8b75ced2b89e5ed9c8ccc6122e9da052cd32191446c0b263aa48ba3574ba40d521d23320a9e337f5961ee876739e6f03cbb1ea347ada055ee969e5e09b5be41dc1df0da6e8d84a0e8c354").unwrap();
    let pt = secret.decrypt(PaddingScheme::PKCS1v15Encrypt, &ct).unwrap();
    println!("{}", String::from_utf8(pt).unwrap());
}
```
Submitting the plaintext to the server (for this particular session) yields the flag.

Flag: `gigem{lol_omg_im_so_random}`


