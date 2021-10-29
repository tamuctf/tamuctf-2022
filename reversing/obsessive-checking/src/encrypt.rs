use aes::cipher::{BlockEncryptMut, KeyIvInit};
use obfstr::obfstr;
use rand::Rng;
use rand_chacha::rand_core::SeedableRng;
use rand_chacha::ChaCha20Rng;
use sha3::{Digest, Sha3_256};
use std::fs::File;
use std::io::{BufReader, BufWriter, Read, Write};

type Aes256CbcEnc = cbc::Encryptor<aes::Aes256>;

fn main() -> anyhow::Result<()> {
    let mut rng = ChaCha20Rng::from_entropy();
    let file = std::env::args().nth(1).unwrap();

    let input = File::open(&file)?;
    let mut reader = BufReader::new(input);

    let output = File::create(file + ".bin")?;
    let mut writer = BufWriter::new(output);

    let mut buf = [0u8; 16];
    let iv: [u8; 16] = rng.gen();

    let mut hasher = Sha3_256::default();
    hasher.update(obfstr!("What a lovely password for this fine evening!").as_bytes());
    let mut cipher = Aes256CbcEnc::new(&hasher.finalize(), &iv.into());

    writer.write_all(&iv)?;

    while let Ok(amount) = reader.read(&mut buf) {
        if amount == 0 {
            break;
        }
        cipher.encrypt_block_mut(buf.as_mut_slice().into());
        writer.write_all(&buf)?;
        buf.fill(0);
    }

    Ok(())
}
