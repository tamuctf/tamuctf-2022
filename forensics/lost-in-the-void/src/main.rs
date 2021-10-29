use rand::SeedableRng;
use rand_chacha::ChaChaRng;
use rsa::{PaddingScheme, PublicKey, RsaPrivateKey, RsaPublicKey};
use tokio::fs::File;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::process::Command;
use zeroize::Zeroizing;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let mut rng = ChaChaRng::from_entropy();
    let key = RsaPrivateKey::new(&mut rng, 4096)?;
    let pubkey = RsaPublicKey::from(&key);

    {
        let mut plaintext = Zeroizing::new(Vec::new());
        File::open("flag.txt").await?.read_to_end(&mut plaintext).await?;

        let ciphertext = Zeroizing::new(pubkey.encrypt(&mut rng, PaddingScheme::PKCS1v15Encrypt, &plaintext)?);
        File::create("enc.bin").await?.write_all(&ciphertext).await?;
    }


    Command::new("gcore").arg(std::process::id().to_string()).spawn().unwrap().wait().await?;

    Ok(())
}
