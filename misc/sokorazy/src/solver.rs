use std::collections::{HashMap, HashSet};
use std::hash::{Hash, Hasher};
use std::iter::repeat;
use std::sync::{Arc, RwLock};
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread::available_parallelism;
use heapless::FnvIndexSet;
use rand::prelude::*;
use rayon::prelude::*;
use sokoban::{Block, Direction, State as SokobanState, State};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader, BufWriter};
use tokio::net::TcpStream;

struct EnrichedState {
    state: State,
    moves: Vec<Direction>,
    positions: Vec<(usize, usize)>,
}

impl Hash for EnrichedState {
    fn hash<H: Hasher>(&self, state: &mut H) {
        to_watched_state(&self.state).hash(state);
    }
}

impl PartialEq<Self> for EnrichedState {
    fn eq(&self, other: &Self) -> bool {
        to_watched_state(&self.state).eq(&to_watched_state(&other.state))
    }
}

impl Eq for EnrichedState {}

fn to_watched_state(state: &State) -> (heapless::Vec<(usize, usize), 8>, (usize, usize)) {
    let all_crates = (0..12).flat_map(|r| {
        repeat(r).zip(0..18).filter(|(r, c)| state[(*r, *c)] == Block::Crate)
    }).collect::<heapless::Vec<_, 8>>();
    (all_crates, state.player())
}

fn is_deadended(state: &State) -> bool {
    let mut crates = Vec::new();
    for row in 0..12 {
        for col in 0..18 {
            if state[(row, col)] == Block::Crate && !state.targets().contains(&(row, col)) {
                // we only care about crates which aren't in the right place
                crates.push((row, col));
            }
        }
    }
    for item in crates {
        let (row, col) = item;
        for (pos1, pos2) in [
            ((row, col + 1), (row + 1, col)),
            ((row, col + 1), (row - 1, col)),
            ((row, col - 1), (row + 1, col)),
            ((row, col - 1), (row - 1, col)),
        ] {
            if state[pos1] == Block::Wall && state[pos2] == Block::Wall {
                // state is deadended; there is no way to move this box
                return true;
            }
        }
    }
    return false;
}

fn l0_dist(pos1: (usize, usize), pos2: (usize, usize)) -> usize {
    pos1.0.abs_diff(pos2.0).checked_sub(1).unwrap_or(0) + pos1.1.abs_diff(pos2.1).checked_sub(1).unwrap_or(0)
}

fn maybe_go(orig: (usize, usize), dir: Direction) -> Option<(usize, usize)> {
    match dir {
        Direction::Up => orig.0.checked_sub(1).map(|v| (v, orig.1)),
        Direction::Down => orig.0.checked_add(1).map(|v| (v, orig.1)),
        Direction::Left => orig.1.checked_sub(1).map(|v| (orig.0, v)),
        Direction::Right => orig.1.checked_add(1).map(|v| (orig.0, v)),
    }
}

fn solve_bfs(state: State) -> Vec<Direction> {
    let init_watched_state = to_watched_state(&state);
    let mut configurations = RwLock::new(HashSet::new());
    configurations.write().unwrap().insert(init_watched_state.clone());
    let mut seen = HashSet::new();
    seen.insert(init_watched_state);
    let mut enriched = HashSet::new();
    enriched.insert(EnrichedState {
        positions: vec![state.player()],
        state,
        moves: Vec::new(),
    });
    let moves = loop {
        if enriched.len() == 0 {
            unreachable!("Deadended.");
        }
        let next = if enriched.len() > 1000 {
            println!("Using threaded solver: {}", enriched.len());
            let mut next = HashSet::with_capacity(enriched.len() * 4);
            for (result, newly_seen) in enriched.into_par_iter().map(|state| {
                let mut next = HashSet::with_capacity(4);
                let mut newly_seen = FnvIndexSet::new();
                step_bfs(state, &mut next, &seen, &configurations, &mut newly_seen);
                (next, newly_seen)
            }).collect::<Vec<_>>() {
                next.extend(result);
                seen.extend(newly_seen.iter().cloned());
            }
            next
        } else {
            let mut next = HashSet::with_capacity(enriched.len() * 4);
            for state in enriched {
                let mut newly_seen = FnvIndexSet::new();
                step_bfs(state, &mut next, &seen, &configurations, &mut newly_seen);
                seen.extend(newly_seen.iter().cloned());
            }
            next
        };
        if let Some(state) = next.iter().find(|&state| state.state.in_solution_state()) {
            break state.moves.clone();
        }
        enriched = next;
    };
    moves
}

fn step_bfs(state: EnrichedState, pool: &mut HashSet<EnrichedState>, seen: &HashSet<(heapless::Vec<(usize, usize), 8>, (usize, usize))>, configurations: &RwLock<HashSet<(heapless::Vec<(usize, usize), 8>, (usize, usize))>>, newly_seen: &mut FnvIndexSet<(heapless::Vec<(usize, usize), 8>, (usize, usize)), 4>) {
    'steploop:
    for dir in [Direction::Left, Direction::Right, Direction::Up, Direction::Down] {
        if let Ok(next_state) = state.state.clone().move_player(dir) {
            let watched_state = to_watched_state(&next_state);
            if state.state[next_state.player()] == Block::Crate {
                // we've just moved a crate; make sure we've not tried this already
                if !configurations.write().unwrap().insert(watched_state.clone()) {
                    return;
                }
            }
            if seen.contains(&watched_state) {
                continue 'steploop;
            }
            newly_seen.insert(watched_state).unwrap();

            // trim deadended states
            if is_deadended(&next_state) {
                continue 'steploop;
            }

            let mut moves = state.moves.clone();
            moves.push(dir);
            let mut positions = state.positions.clone();
            positions.push(next_state.player());
            pool.insert(EnrichedState {
                state: next_state,
                moves,
                positions,
            });
        }
    }
}

fn solve_dfs<const MAX_DEPTH: usize>(state: State, should_continue: Arc<AtomicBool>) -> Option<Vec<Direction>> {
    let init_watched_state = to_watched_state(&state);
    let mut configurations = HashSet::new();
    configurations.insert(init_watched_state.0.clone());
    let mut seen = HashMap::new();
    seen.insert(init_watched_state, 0);
    let mut stack = heapless::Vec::<(State, heapless::Vec<Direction, 4>), MAX_DEPTH>::new();
    let mut moves = Vec::new();
    stack.push((state, heapless::Vec::from_slice(&[Direction::Left, Direction::Right, Direction::Up, Direction::Down]).unwrap())).unwrap();
    let mut rng = thread_rng();
    loop {
        if !should_continue.load(Ordering::Relaxed) {
            return None;
        }
        if stack.len() == 0 {
            unreachable!("Deadended.");
        }

        step_dfs(&mut stack, &mut seen, &mut configurations, &mut moves, &mut rng);

        if stack.last().unwrap().0.in_solution_state() {
            break;
        }
    };
    should_continue.store(false, Ordering::Relaxed);
    Some(moves)
}

fn step_dfs<const MAX_DEPTH: usize>(stack: &mut heapless::Vec<(State, heapless::Vec<Direction, 4>), MAX_DEPTH>, seen: &mut HashMap<(heapless::Vec<(usize, usize), 8>, (usize, usize)), usize>, configurations: &mut HashSet<heapless::Vec<(usize, usize), 8>>, moves: &mut Vec<Direction>, rng: &mut ThreadRng) {
    let mut popped = false;
    while stack.last().unwrap().1.is_empty() {
        stack.pop();
        moves.pop();
        popped = true;
    }
    if popped {
        // we've just removed some states; clear the seen list
        let crates = stack.iter().map(|s| &s.0).map(to_watched_state).map(|s| s.0).collect::<HashSet<_>>();
        seen.retain(|s, _| crates.contains(&s.0));
    }
    let dir = stack.last_mut().unwrap().1.pop().unwrap();
    if let Ok(next_state) = stack.last().unwrap().0.clone().move_player(dir) {
        let watched_state = to_watched_state(&next_state);
        if stack.last().unwrap().0[next_state.player()] == Block::Crate {
            // we've just moved a crate; make sure we've not tried this already
            if !configurations.insert(watched_state.0.clone()) {
                return;
            }
        }

        if *seen.entry(watched_state).and_modify(|existing| if *existing > stack.len() { *existing = stack.len() }).or_insert(stack.len()) < stack.len() {
            return;
        }

        // trim deadended
        if is_deadended(&next_state) {
            return;
        }

        let mut dirs = heapless::Vec::from_slice(&[Direction::Left, Direction::Right, Direction::Up, Direction::Down]).unwrap();
        dirs.shuffle(rng);

        if stack.push((next_state, dirs)).is_ok() {
            moves.push(dir);
        }
    }
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let mut client = TcpStream::connect("127.0.0.1:7304").await?;
    let (rx, tx) = client.split();
    let mut reader = BufReader::new(rx);
    let mut writer = BufWriter::new(tx);

    {
        let mut discard = String::new();
        reader.read_line(&mut discard).await?;
        reader.read_line(&mut discard).await?;
        reader.read_line(&mut discard).await?;
    }

    for _ in 1..=25 {
        {
            let mut discard = String::new();
            reader.read_line(&mut discard).await?;
            reader.read_line(&mut discard).await?;
            reader.read_line(&mut discard).await?;
        }
        let mut map = String::new();
        for _ in 0..12 {
            reader.read_line(&mut map).await?;
            map.truncate(map.len() - 1);
        }
        let dim_r = 12;
        let dim_c = 18;
        let container = map
            .chars()
            .map(|c| match c {
                '#' => Block::Wall,
                '_' | '.' | 'x' | 'X' => Block::Floor,
                'm' | 'M' => Block::Crate,
                _ => unreachable!("Illegal value in response."),
            })
            .collect::<Vec<_>>();
        let player = map
            .char_indices()
            .find(|(_, c)| *c == 'x' || *c == 'X')
            .expect("Couldn't find the player")
            .0;

        let player = (player / dim_c, player % dim_c);
        let targets = map
            .char_indices()
            .filter_map(|(i, c)| (c.is_ascii_uppercase() || c == '.').then(|| i))
            .map(|i| (i / dim_c, i % dim_c))
            .collect::<Vec<_>>();

        let state = SokobanState::new(container, player, targets, dim_r, dim_c)
            .expect("Expected a valid state from remote");
        println!("{:?}", state);

/*
        let cpus = available_parallelism()?.get();
        let should_continue = Arc::new(AtomicBool::new(true));
        let moves = (0..cpus).divvy(cpus).find_map_any(|_| {
            solve_dfs::<1000>(state.clone(), should_continue.clone())
        }).unwrap();
 */
        let moves = solve_bfs(state);

        println!("{:?}", moves);

        let rendered = moves.into_iter().map(|dir| {
            match dir {
                Direction::Left => b'<',
                Direction::Right => b'>',
                Direction::Up => b'^',
                Direction::Down => b'v',
            }
        }).collect::<Vec<_>>();
        writer.write_all(&rendered).await?;
        writer.write_u8(b'\n').await?;
        writer.flush().await?;
    }

    let mut flag = String::new();
    loop {
        reader.read_line(&mut flag).await?;
        if flag.contains("gigem") {
            break;
        }
        flag.clear();
    }

    println!("{}", flag);

    Ok(())
}
