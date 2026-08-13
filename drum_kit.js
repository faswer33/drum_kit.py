// drum_kit.js — JavaScript версия

const readline = require('readline');

class DrumKit {
    constructor(bpm = 120) {
        this.bpm = bpm;
        this.beatLen = 60 / bpm;
        this.running = false;
        this.pattern = [];
        this.drums = {
            bd: { name: 'Бас', key: '1', symbol: '█' },
            sd: { name: 'Малый', key: '2', symbol: '▓' },
            hh: { name: 'Хай-хэт', key: '3', symbol: '▒' },
            t1: { name: 'Том 1', key: '4', symbol: '░' },
            t2: { name: 'Том 2', key: '5', symbol: '░' },
            rd: { name: 'Райд', key: '6', symbol: '●' },
            cr: { name: 'Крэш', key: '7', symbol: '◆' }
        };
    }

    generateRockPattern(style = 'shuffle') {
        const pattern = [];
        if (style === 'shuffle') {
            for (let i = 0; i < 16; i++) {
                const beat = { bd: 0, sd: 0, hh: 0, t1: 0, t2: 0, rd: 0, cr: 0 };
                if (i % 8 === 0 || i % 8 === 4) beat.bd = 1;
                if (i % 8 === 2 || i % 8 === 6) beat.sd = 1;
                if (i % 2 === 0) beat.hh = 1;
                pattern.push(beat);
            }
        } else {
            for (let i = 0; i < 16; i++) {
                const beat = { bd: 0, sd: 0, hh: 0, t1: 0, t2: 0, rd: 0, cr: 0 };
                if (i % 8 === 0) { beat.bd = 1; beat.cr = 1; }
                if (i % 8 === 4) beat.bd = 1;
                if (i % 8 === 2 || i % 8 === 6) beat.sd = 1;
                if (i % 4 === 0) beat.hh = 1;
                pattern.push(beat);
            }
        }
        return pattern;
    }

    playBeat(beat) {
        let line = '';
        for (const [key, drum] of Object.entries(this.drums)) {
            if (beat[key]) {
                line += `\x1b[32m${drum.symbol}\x1b[0m `;
            } else {
                line += '  ';
            }
        }
        return line;
    }

    displayTimeline() {
        for (const drum of Object.values(this.drums)) {
            process.stdout.write(`${drum.name} `);
        }
        console.log('\n─────────────────────────');
    }

    run(style = 'shuffle') {
        this.pattern = this.generateRockPattern(style);
        this.running = true;

        console.log('\x1b[36m🥁 Rock Drum Kit (JavaScript)\x1b[0m');
        console.log(`Темп: ${this.bpm} BPM`);
        console.log(`Стиль: ${style}`);
        console.log('Нажмите Ctrl+C для остановки...\n');

        this.displayTimeline();

        let beatIndex = 0;
        const interval = setInterval(() => {
            if (!this.running) {
                clearInterval(interval);
                return;
            }
            const beat = this.pattern[beatIndex];
            const line = this.playBeat(beat);
            const bar = Math.floor(beatIndex / 4) + 1;
            const beatInBar = (beatIndex % 4) + 1;
            console.log(`${bar}.${beatInBar}  ${line}`);
            beatIndex = (beatIndex + 1) % this.pattern.length;
        }, this.beatLen / 2 * 1000);

        process.on('SIGINT', () => {
            this.running = false;
            clearInterval(interval);
            console.log('\n⏹️ Остановка...');
            process.exit(0);
        });
    }
}

function main() {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    console.log('🥁 Rock Drum Kit (JavaScript)');
    console.log('Выберите стиль (shuffle/straight):');
    rl.question('> ', (style) => {
        rl.close();
        const drum = new DrumKit(120);
        if (style !== 'shuffle' && style !== 'straight') style = 'shuffle';
        drum.run(style);
    });
}

if (require.main === module) main();
