// drum_kit.rs — Rust версия

use std::collections::HashMap;
use std::time::{Duration, Instant};
use std::thread;

struct Drum {
    name: String,
    key: String,
    symbol: String,
}

struct DrumKit {
    bpm: u32,
    beat_len: f64,
    running: bool,
    pattern: Vec<HashMap<String, u8>>,
    drums: HashMap<String, Drum>,
}

impl DrumKit {
    fn new(bpm: u32) -> Self {
        let mut drums = HashMap::new();
        drums.insert("bd".to_string(), Drum { name: "Бас".to_string(), key: "1".to_string(), symbol: "█".to_string() });
        drums.insert("sd".to_string(), Drum { name: "Малый".to_string(), key: "2".to_string(), symbol: "▓".to_string() });
        drums.insert("hh".to_string(), Drum { name: "Хай-хэт".to_string(), key: "3".to_string(), symbol: "▒".to_string() });
        drums.insert("t1".to_string(), Drum { name: "Том 1".to_string(), key: "4".to_string(), symbol: "░".to_string() });
        drums.insert("t2".to_string(), Drum { name: "Том 2".to_string(), key: "5".to_string(), symbol: "░".to_string() });
        drums.insert("rd".to_string(), Drum { name: "Райд".to_string(), key: "6".to_string(), symbol: "●".to_string() });
        drums.insert("cr".to_string(), Drum { name: "Крэш".to_string(), key: "7".to_string(), symbol: "◆".to_string() });

        DrumKit {
            bpm,
            beat_len: 60.0 / bpm as f64,
            running: false,
            pattern: Vec::new(),
            drums,
        }
    }

    fn generate_rock_pattern(&mut self, style: &str) {
        let mut pattern = Vec::new();
        if style == "shuffle" {
            for i in 0..16 {
                let mut beat = HashMap::new();
                beat.insert("bd".to_string(), 0);
                beat.insert("sd".to_string(), 0);
                beat.insert("hh".to_string(), 0);
                beat.insert("t1".to_string(), 0);
                beat.insert("t2".to_string(), 0);
                beat.insert("rd".to_string(), 0);
                beat.insert("cr".to_string(), 0);
                if i % 8 == 0 || i % 8 == 4 { beat.insert("bd".to_string(), 1); }
                if i % 8 == 2 || i % 8 == 6 { beat.insert("sd".to_string(), 1); }
                if i % 2 == 0 { beat.insert("hh".to_string(), 1); }
                pattern.push(beat);
            }
        } else {
            for i in 0..16 {
                let mut beat = HashMap::new();
                beat.insert("bd".to_string(), 0);
                beat.insert("sd".to_string(), 0);
                beat.insert("hh".to_string(), 0);
                beat.insert("t1".to_string(), 0);
                beat.insert("t2".to_string(), 0);
                beat.insert("rd".to_string(), 0);
                beat.insert("cr".to_string(), 0);
                if i % 8 == 0 { beat.insert("bd".to_string(), 1); beat.insert("cr".to_string(), 1); }
                if i % 8 == 4 { beat.insert("bd".to_string(), 1); }
                if i % 8 == 2 || i % 8 == 6 { beat.insert("sd".to_string(), 1); }
                if i % 4 == 0 { beat.insert("hh".to_string(), 1); }
                pattern.push(beat);
            }
        }
        self.pattern = pattern;
    }

    fn play_beat(&self, beat: &HashMap<String, u8>) -> String {
        let mut line = String::new();
        for (key, drum) in &self.drums {
            if let Some(&val) = beat.get(key) {
                if val == 1 {
                    line.push_str(&format!("\x1b[32m{}\x1b[0m ", drum.symbol));
                } else {
                    line.push_str("  ");
                }
            } else {
                line.push_str("  ");
            }
        }
        line
    }

    fn display_timeline(&self) {
        for drum in self.drums.values() {
            print!("{} ", drum.name);
        }
        println!("\n─────────────────────────");
    }

    fn run(&mut self, style: &str) {
        self.generate_rock_pattern(style);
        self.running = true;

        println!("\x1b[36m🥁 Rock Drum Kit (Rust)\x1b[0m");
        println!("Темп: {} BPM", self.bpm);
        println!("Стиль: {}", style);
        println!("Нажмите Ctrl+C для остановки...\n");

        self.display_timeline();

        let beat_len_ms = (self.beat_len / 2.0 * 1000.0) as u64;
        let mut beat_index = 0;

        loop {
            let beat = &self.pattern[beat_index];
            let line = self.play_beat(beat);
            let bar = beat_index / 4 + 1;
            let beat_in_bar = beat_index % 4 + 1;
            println!("{}.{}  {}", bar, beat_in_bar, line);
            beat_index = (beat_index + 1) % self.pattern.len();
            thread::sleep(Duration::from_millis(beat_len_ms));
        }
    }
}

fn main() {
    println!("🥁 Rock Drum Kit (Rust)");
    println!("Стиль (shuffle/straight): ");
    let mut style = String::new();
    std::io::stdin().read_line(&mut style).unwrap();
    let style = style.trim();
    let style = if style == "shuffle" || style == "straight" { style } else { "shuffle" };

    let mut kit = DrumKit::new(120);
    kit.run(style);
}
