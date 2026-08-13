<?php
// drum_kit.php — PHP версия

class DrumKit {
    private $bpm;
    private $beatLen;
    private $running;
    private $pattern;
    private $drums;

    public function __construct($bpm = 120) {
        $this->bpm = $bpm;
        $this->beatLen = 60 / $bpm;
        $this->running = false;
        $this->drums = [
            'bd' => ['name' => 'Бас', 'key' => '1', 'symbol' => '█'],
            'sd' => ['name' => 'Малый', 'key' => '2', 'symbol' => '▓'],
            'hh' => ['name' => 'Хай-хэт', 'key' => '3', 'symbol' => '▒'],
            't1' => ['name' => 'Том 1', 'key' => '4', 'symbol' => '░'],
            't2' => ['name' => 'Том 2', 'key' => '5', 'symbol' => '░'],
            'rd' => ['name' => 'Райд', 'key' => '6', 'symbol' => '●'],
            'cr' => ['name' => 'Крэш', 'key' => '7', 'symbol' => '◆']
        ];
    }

    private function generateRockPattern($style) {
        $pattern = [];
        if ($style == 'shuffle') {
            for ($i = 0; $i < 16; $i++) {
                $beat = ['bd' => 0, 'sd' => 0, 'hh' => 0, 't1' => 0, 't2' => 0, 'rd' => 0, 'cr' => 0];
                if ($i % 8 == 0 || $i % 8 == 4) $beat['bd'] = 1;
                if ($i % 8 == 2 || $i % 8 == 6) $beat['sd'] = 1;
                if ($i % 2 == 0) $beat['hh'] = 1;
                $pattern[] = $beat;
            }
        } else {
            for ($i = 0; $i < 16; $i++) {
                $beat = ['bd' => 0, 'sd' => 0, 'hh' => 0, 't1' => 0, 't2' => 0, 'rd' => 0, 'cr' => 0];
                if ($i % 8 == 0) { $beat['bd'] = 1; $beat['cr'] = 1; }
                if ($i % 8 == 4) $beat['bd'] = 1;
                if ($i % 8 == 2 || $i % 8 == 6) $beat['sd'] = 1;
                if ($i % 4 == 0) $beat['hh'] = 1;
                $pattern[] = $beat;
            }
        }
        return $pattern;
    }

    private function playBeat($beat) {
        $line = '';
        foreach ($this->drums as $key => $drum) {
            if ($beat[$key] == 1) {
                $line .= "\033[32m{$drum['symbol']}\033[0m ";
            } else {
                $line .= '  ';
            }
        }
        return $line;
    }

    private function displayTimeline() {
        foreach ($this->drums as $drum) {
            echo $drum['name'] . ' ';
        }
        echo "\n─────────────────────────\n";
    }

    public function run($style) {
        $this->pattern = $this->generateRockPattern($style);
        $this->running = true;

        echo "\033[36m🥁 Rock Drum Kit (PHP)\033[0m\n";
        echo "Темп: {$this->bpm} BPM\n";
        echo "Стиль: $style\n";
        echo "Нажмите Ctrl+C для остановки...\n\n";

        $this->displayTimeline();

        $beatIndex = 0;
        $patternLen = count($this->pattern);

        pcntl_signal(SIGINT, function() {
            $this->running = false;
            echo "\n⏹️ Остановка...\n";
            exit(0);
        });

        while ($this->running) {
            $beat = $this->pattern[$beatIndex];
            $line = $this->playBeat($beat);
            $bar = intdiv($beatIndex, 4) + 1;
            $beatInBar = $beatIndex % 4 + 1;
            echo "$bar.$beatInBar  $line\n";
            $beatIndex = ($beatIndex + 1) % $patternLen;
            usleep($this->beatLen / 2 * 1000000);
            pcntl_signal_dispatch();
        }
    }
}

function main() {
    echo "🥁 Rock Drum Kit (PHP)\n";
    echo "Стиль (shuffle/straight): ";
    $style = trim(fgets(STDIN));
    $style = strtolower($style);
    if ($style != 'shuffle' && $style != 'straight') $style = 'shuffle';

    $kit = new DrumKit(120);
    $kit->run($style);
}

main();
?>
