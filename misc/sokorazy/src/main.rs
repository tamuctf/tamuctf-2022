use anyhow::Error;
use rand::{RngCore, SeedableRng};
use rand_chacha::ChaChaRng;
use serde::{Deserialize, Serialize};
use serde_xml_rs::from_str;
use sokoban::{Block, Direction, State as SokobanState};
use std::net::SocketAddr;
use std::time::SystemTime;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, TcpStream};
use tokio::sync::{mpsc, oneshot};

#[derive(Debug, Deserialize, Serialize, PartialEq)]
struct Response {
    deal: String,
}

impl From<Response> for SokobanState {
    fn from(resp: Response) -> Self {
        let dim_r = 12;
        let dim_c = 18;
        let container = resp
            .deal
            .chars()
            .map(|c| match c {
                'w' => Block::Wall,
                'e' | 'E' | 'm' | 'M' => Block::Floor,
                'o' | 'O' => Block::Crate,
                _ => unreachable!("Illegal value in response."),
            })
            .collect::<Vec<_>>();
        let player = resp
            .deal
            .char_indices()
            .find(|(_, c)| *c == 'm' || *c == 'M')
            .expect("Couldn't find the player")
            .0;

        let player = (player / dim_c, player % dim_c);
        let targets = resp
            .deal
            .char_indices()
            .filter_map(|(i, c)| c.is_ascii_uppercase().then(|| i))
            .map(|i| (i / dim_c, i % dim_c))
            .collect::<Vec<_>>();
        SokobanState::new(container, player, targets, dim_r, dim_c)
            .expect("Expected a valid state from remote")
    }
}

async fn handle_user_inner(
    conn: &mut TcpStream,
    addr: SocketAddr,
    seed: u32,
    tx: mpsc::Sender<(u32, usize, oneshot::Sender<anyhow::Result<Response>>)>,
) -> anyhow::Result<()> {
    conn.write_all(
        br#"Welcome to the sokoban guantlet!
You must solve 25 sokoban puzzles in 10 minutes without error to get the flag.
Puzzles take some time to generate, so please be patient between challenges.

"#,
    )
    .await?;
    conn.flush().await?;
    let start_time = SystemTime::now();
    for level in 0..25 {
        println!("{} advanced to level {}!", addr, level);
        conn.write_all(b"Generating next puzzle...\n").await?;
        conn.flush().await?;
        let (req_tx, req_rx) = oneshot::channel();
        tx.send((seed, level, req_tx)).await?;
        let resp = match req_rx.await? {
            Ok(r) => r,
            Err(e) => {
                eprintln!("{:?}", e);
                return Err(Error::msg(
                    "Couldn't generate the sokoban puzzle; contact an administrator.",
                ))
            }
        };
        conn.write_all(b"Here's your next challenge:").await?;
        conn.flush().await?;
        let mut state = SokobanState::from(resp);
        conn.write_all(format!("{:?}", state).as_bytes()).await?;
        conn.flush().await?;

        loop {
            let c = conn.read_u8().await?;
            let dir = match c {
                b'^' => Direction::Up,
                b'v' => Direction::Down,
                b'>' => Direction::Right,
                b'<' => Direction::Left,
                b'\n' => break,
                c => return Err(Error::msg(format!("Invalid move character: {}", c))),
            };
            state = state.move_player(dir)?;
        }

        if state.in_solution_state() {
            conn.write_all(b"Correct!\n").await?;
        } else {
            return Err(Error::msg("Puzzle was not in solution state."));
        }
    }

    if start_time.elapsed()?.as_secs() < 600 {
        conn.write_all(b"gigem{dm_addison_if_you_are_interested_in_more_challenges_like_this}\n").await?;
        conn.flush().await?;
    }

    Ok(())
}

async fn handle_user(
    mut conn: TcpStream,
    addr: SocketAddr,
    seed: u32,
    tx: mpsc::Sender<(u32, usize, oneshot::Sender<anyhow::Result<Response>>)>,
) {
    if let Err(e) = handle_user_inner(&mut conn, addr, seed, tx).await {
        let _ = conn
            .write_all(format!("Encountered error while processing: {}\n", e).as_bytes())
            .await;
        println!(
            "Encountered error while processing from address {}: {}",
            addr, e
        );
    }
}

async fn do_sokoban_request_inner(seed: u32, level: usize) -> anyhow::Result<Response> {
    let resp = reqwest::get(format!(
        "http://www.linusakesson.net/games/autosokoban/board.php?v=1&seed={}&level={}",
        seed, level
    ))
    .await?
    .text()
    .await?;

    let resp: Response = from_str(&resp)?;

    Ok(resp)
}

async fn do_sokoban_request(
    seed: u32,
    level: usize,
    tx: oneshot::Sender<anyhow::Result<Response>>,
) {
    tx.send(do_sokoban_request_inner(seed, level).await)
        .expect("Couldn't send sokoban result");
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let mut rng = ChaChaRng::from_entropy();
    let server = TcpListener::bind("0.0.0.0:7304").await?;

    // only one sokoban puzzle generated at a time globally
    let (tx, mut rx) = mpsc::channel(1);
    tokio::spawn(async move {
        while let Some((seed, level, tx)) = rx.recv().await {
            do_sokoban_request(seed, level, tx).await;
        }
    });

    while let Ok((conn, addr)) = server.accept().await {
        let seed = rng.next_u32();
        println!("Starting user session for {} with seed {}", addr, seed);
        let tx = tx.clone();

        tokio::spawn(async move {
            handle_user(conn, addr, seed, tx).await;
        });
    }

    Ok(())
}
