// drum_kit.cs — C# версия

using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

class Drum {
    public string Name { get; set; }
    public string Key { get; set; }
    public string Symbol { get; set; }
}

class DrumKit {
    private int bpm;
    private double beatLen;
    private bool running;
    private List<Dictionary<string, int>> pattern;
    private Dictionary<string, Drum> drums;

    public DrumKit(int bpm) {
        this.bpm = bpm;
        this.beatLen = 60.0 / bpm;
        this.drums = new Dictionary<string, Drum> {
            {"bd", new Drum{Name="Бас", Key="1", Symbol="█"}},
            {"sd", new Drum{Name="Малый", Key="2", Symbol="▓"}},
            {"hh", new Drum{Name="Хай-хэт", Key="3", Symbol="▒"}},
            {"t1", new Drum{Name="Том 1", Key="4", Symbol="░"}},
            {"t2", new Drum{Name="Том 2", Key="5", Symbol="░"}},
            {"rd", new Drum{Name="Райд", Key="6", Symbol="●"}},
            {"cr", new Drum{Name="Крэш", Key="7", Symbol="◆"}}
        };
    }

    private List<Dictionary<string, int>> GenerateRockPattern(string style) {
        var pattern = new List<Dictionary<string, int>>();
        if (style == "shuffle") {
            for (int i = 0; i < 16; i++) {
                var beat = new Dictionary<string, int> {{"bd",0},{"sd",0},{"hh",0},{"t1",0},{"t2",0},{"rd",0},{"cr",0}};
                if (i % 8 == 0 || i % 8 == 4) beat["bd"] = 1;
                if (i % 8 == 2 || i % 8 == 6) beat["sd"] = 1;
                if (i % 2 == 0) beat["hh"] = 1;
                pattern.Add(beat);
            }
        } else {
            for (int i = 0; i < 16; i++) {
                var beat = new Dictionary<string, int> {{"bd",0},{"sd",0},{"hh",0},{"t1",0},{"t2",0},{"rd",0},{"cr",0}};
                if (i % 8 == 0) { beat["bd"] = 1; beat["cr"] = 1; }
                if (i % 8 == 4) beat["bd"] = 1;
                if (i % 8 == 2 || i % 8 == 6) beat["sd"] = 1;
                if (i % 4 == 0) beat["hh"] = 1;
                pattern.Add(beat);
            }
        }
        return pattern;
    }

    private string PlayBeat(Dictionary<string, int> beat) {
        string line = "";
        foreach (var kv in drums) {
            if (beat.GetValueOrDefault(kv.Key, 0) == 1) {
                line += $"\x1b[32m{kv.Value.Symbol}\x1b[0m ";
            } else {
                line += "  ";
            }
        }
        return line;
    }

    private void DisplayTimeline() {
        foreach (var d in drums.Values) {
            Console.Write($"{d.Name} ");
        }
        Console.WriteLine("\n─────────────────────────");
    }

    public void Run(string style) {
        this.pattern = GenerateRockPattern(style);
        this.running = true;

        Console.WriteLine($"\x1b[36m🥁 Rock Drum Kit (C#)\x1b[0m");
        Console.WriteLine($"Темп: {bpm} BPM");
        Console.WriteLine($"Стиль: {style}");
        Console.WriteLine("Нажмите Ctrl+C для остановки...\n");

        DisplayTimeline();

        int beatIndex = 0;
        var timer = new Timer(_ => {
            if (!running) return;
            var beat = pattern[beatIndex];
            string line = PlayBeat(beat);
            int bar = beatIndex / 4 + 1;
            int beatInBar = beatIndex % 4 + 1;
            Console.WriteLine($"{bar}.{beatInBar}  {line}");
            beatIndex = (beatIndex + 1) % pattern.Count;
        }, null, 0, (int)(beatLen / 2 * 1000));

        Console.CancelKeyPress += (sender, e) => {
            e.Cancel = true;
            running = false;
            timer.Dispose();
            Console.WriteLine("\n⏹️ Остановка...");
        };

        Thread.Sleep(Timeout.Infinite);
    }

    public static void Main() {
        Console.WriteLine("🥁 Rock Drum Kit (C#)");
        Console.Write("Стиль (shuffle/straight): ");
        string style = Console.ReadLine()?.Trim().ToLower();
        if (style != "shuffle" && style != "straight") style = "shuffle";
        var kit = new DrumKit(120);
        kit.Run(style);
    }
}
