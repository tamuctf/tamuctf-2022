use std::sync::Arc;
use std::time::{Duration, SystemTime};

use aes::cipher::{BlockDecryptMut, KeyIvInit};
use obfstr::obfstr;
use rand::{Rng, SeedableRng};
use rand_chacha::ChaCha20Rng;
use sha3::{Digest, Sha3_256};
use tokio::{
    fs::File,
    io::{AsyncReadExt, BufReader},
    sync::{mpsc, Semaphore},
};

type Aes256CbcDec = cbc::Decryptor<aes::Aes256>;

const MAX_CHECKS: usize = 64;

async fn check_task(tx: mpsc::Sender<SystemTime>, sem: Arc<Semaphore>) {
    while let Ok(permit) = sem.acquire().await {
        let t = SystemTime::now();
        if tx.send(t).await.is_err() {
            panic!("{}", obfstr!("couldn't send time check"))
        }
        permit.forget();
    }
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let file = std::env::args().nth(1);
    if file.is_none() {
        println!(
            "{}",
            obfstr!("Couldn't find the file you're referencing. Maybe you meant a different file?")
        );
    }
    let file = File::open(file.unwrap()).await?;
    let mut reader = BufReader::new(file);

    let mut iv = [0; 16];
    reader.read_exact(&mut iv).await?;

    let mut hasher = Sha3_256::default();
    hasher.update(obfstr!("What a lovely password for this fine evening!").as_bytes());
    let mut cipher = Aes256CbcDec::new(&hasher.finalize(), &iv.into());

    let (check_tx, mut check_rx) = mpsc::channel(MAX_CHECKS);

    let sem = Arc::new(Semaphore::new(0));
    let mut checkers = Vec::with_capacity(MAX_CHECKS);

    for _ in 0..MAX_CHECKS {
        checkers.push(tokio::spawn(check_task(check_tx.clone(), sem.clone())));
    }
    drop(check_tx);

    let mut buf = [0u8; 16];
    let mut curr = Vec::new();
    let mut rng = ChaCha20Rng::from_entropy();
    let mut prev = SystemTime::now();
    let mut last = prev;
    while reader.read_exact(&mut buf).await.is_ok() {
        cipher.decrypt_block_mut(buf.as_mut_slice().into());
        curr.extend_from_slice(&buf);
        while let Some((pos, &c)) = curr
            .iter()
            .enumerate()
            .find(|(_, &c)| c == b'\n' || c == b'\0')
        {
            while prev
                .duration_since(last)
                .map_or(false, |elapsed| elapsed < Duration::from_secs(2))
            {
                let count = rng.gen_range((MAX_CHECKS / 2)..MAX_CHECKS);
                sem.add_permits(count);
                let mut min = check_rx.recv().await.unwrap();
                let mut max = min;
                for _ in 1..count {
                    let next = check_rx.recv().await.unwrap();
                    if next > max {
                        max = next;
                    } else if next < min {
                        min = next;
                    }
                }
                let jitter = max.duration_since(min).unwrap();
                if jitter > Duration::from_millis(20) {
                    panic!("{}", obfstr!("suspicious jitter detected"));
                }
                prev = max;
            }
            let line = String::from_utf8_lossy(&curr[..pos]);
            println!("{}", line);
            if c == b'\0' {
                break;
            }
            curr.drain(..=pos);
            last = prev;
        }
    }

    sem.close();
    drop(check_rx);
    for checker in checkers {
        checker.await.unwrap();
    }

    Ok(())
}
